#!/bin/bash
# ============================================================================
# Shared Library for Python Starter Kit Git Hooks
# Provides common utilities: dependency checking, logging, caching, parallel exec
# ============================================================================

# Prevent double-include
if [[ -n "${_SHARED_LIB_LOADED:-}" ]]; then
    return 0
fi
_SHARED_LIB_LOADED=1

# ============================================================================
# Configuration
# ============================================================================
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)")"
HOOKS_DIR="${PROJECT_ROOT}/.githooks"
CACHE_DIR="${PROJECT_ROOT}/.git/.hooks-cache"
REPORT_DIR="${PROJECT_ROOT}/build/reports/pre-commit"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
CACHE_TTL=300  # 5 minutes cache TTL

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'
BOLD='\033[1m'
DIM='\033[2m'

# ============================================================================
# State
# ============================================================================
PASS=true
STAGED_FILES=""
CURRENT_BRANCH=""

# ============================================================================
# Initialization
# ============================================================================
init_hook() {
    cd "${PROJECT_ROOT}" 2>/dev/null || {
        echo -e "  ${RED}✗${NC} Failed to change to project root: ${PROJECT_ROOT}"
        return 1
    }
    mkdir -p "${CACHE_DIR}" "${REPORT_DIR}"
    CURRENT_BRANCH=$(git symbolic-ref HEAD 2>/dev/null | sed 's|refs/heads/||')
    STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACMR 2>/dev/null || echo "")
}

# ============================================================================
# Terminal Output
# ============================================================================
print_banner() {
    local title="$1"
    local color="${2:-${CYAN}}"
    echo -e "\n${color}${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${color}${BOLD}║     ${title}${NC}"
    echo -e "${color}${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_section() {
    local section_num="$1"
    local total="$2"
    local icon="$3"
    local title="$4"
    echo -e "\n${YELLOW}${BOLD}═══ ${section_num}/${total} ${icon}  ${title} ═══${NC}\n"
}

print_pass() {
    echo -e "  ${GREEN}✓${NC} $1"
}

print_warn() {
    echo -e "  ${YELLOW}⚠${NC} $1"
}

print_fail() {
    echo -e "  ${RED}✗${NC} $1"
    PASS=false
}

print_info() {
    echo -e "  ${CYAN}ℹ${NC} $1"
}

print_detail() {
    echo -e "  ${DIM}$1${NC}"
}

print_timing() {
    local elapsed=$1
    local label="$2"
    if (( elapsed >= 10 )); then
        echo -e "  ${DIM}⏱ ${label}: ${elapsed}s${NC}"
    fi
}

# ============================================================================
# Dependency Checking
# ============================================================================

# Check if a specific tool/command exists
check_tool() {
    local tool_name="$1"
    local command="${2:-${tool_name}}"
    if command -v "${command}" &>/dev/null; then
        return 0
    fi
    return 1
}

# Check required tools and report which ones are missing
check_required_tools() {
    local required_tools=("$@")
    local missing=0
    local missing_details=""

    for tool in "${required_tools[@]}"; do
        if ! command -v "${tool}" &>/dev/null; then
            missing=$((missing + 1))
            missing_details+="    ${RED}✗${NC} ${tool} - not found\n"
        fi
    done

    if (( missing > 0 )); then
        echo -e "\n  ${RED}${BOLD}Missing Required Tools (${missing}):${NC}"
        echo -e "${missing_details}"
        return 1
    fi

    return 0
}

# Check all dependencies for Python monorepo
check_all_dependencies() {
    local check_type="${1:-all}"
    local all_ok=true

    print_info "Checking system dependencies..."

    # Essential tools
    local essentials=("git" "bash" "grep" "sed" "awk" "xargs" "find" "sort")
    if ! check_required_tools "${essentials[@]}"; then
        all_ok=false
    fi

    # Check uv
    if ! command -v uv &>/dev/null; then
        print_warn "uv not found - install from https://docs.astral.sh/uv/"
        print_detail "       curl -LsSf https://astral.sh/uv/install.sh | sh"
    fi

    # Check python
    if ! command -v python3 &>/dev/null; then
        print_warn "python3 not found"
    fi

    if [[ "${all_ok}" == "false" ]]; then
        echo -e "\n  ${YELLOW}Fix missing dependencies and re-run the hook.${NC}"
        echo -e "  ${YELLOW}To bypass: git commit --no-verify${NC}"
        return 1
    fi

    print_pass "All required dependencies found"
    return 0
}

# ============================================================================
# Caching
# ============================================================================
cache_get() {
    local key="$1"
    local cache_file="${CACHE_DIR}/${key}"
    if [[ -f "${cache_file}" ]]; then
        local cache_age
        cache_age=$(( $(date +%s) - $(stat -f%m "${cache_file}" 2>/dev/null || stat -c%Y "${cache_file}" 2>/dev/null) ))
        if (( cache_age < CACHE_TTL )); then
            cat "${cache_file}"
            return 0
        fi
    fi
    return 1
}

cache_set() {
    local key="$1"
    local value="$2"
    echo "${value}" > "${CACHE_DIR}/${key}" 2>/dev/null || true
}

# ============================================================================
# Staged File Analysis
# ============================================================================
get_staged_files() {
    echo "${STAGED_FILES}"
}

get_staged_count() {
    if [[ -z "${STAGED_FILES}" ]]; then
        echo "0"
    else
        echo "${STAGED_FILES}" | wc -l | tr -d ' '
    fi
}

staged_files_match() {
    local pattern="$1"
    echo "${STAGED_FILES}" | grep -qE "${pattern}" 2>/dev/null
    return $?
}

has_python_files() {
    staged_files_match "\.py$"
}

has_config_files() {
    staged_files_match "\.(yml|yaml|json|toml|ini|cfg)$"
}

has_docker_files() {
    staged_files_match "Dockerfile|docker-compose"
}

# ============================================================================
# Content Scanning
# ============================================================================
scan_for_secrets() {
    local files="$1"
    local found_any=false

    local patterns=(
        'password\s*[=:]\s*['"'"'"]?\S+'
        'secret\s*[=:]\s*['"'"'"]?\S+'
        'api[_-]?key\s*[=:]\s*['"'"'"]?\S+'
        'api[_-]?secret\s*[=:]\s*['"'"'"]?\S+'
        'access[_-]?key\s*[=:]\s*['"'"'"]?\S+'
        'private[_-]?key\s*[=:]\s*['"'"'"]?\S+'
        'token\s*[=:]\s*['"'"'"]?\S+'
        'AKIA[0-9A-Z]{16}'
        '-----BEGIN (RSA |EC )?PRIVATE KEY-----'
        'ghp_[A-Za-z0-9]{36}'
        'sk-[A-Za-z0-9]{32,}'
    )

    echo "${files}" | while IFS= read -r file; do
        [[ -z "${file}" ]] && continue
        [[ ! -f "${file}" ]] && continue
        if file "${file}" | grep -qi "binary"; then
            continue
        fi
        for pattern in "${patterns[@]}"; do
            if grep -lqE "${pattern}" "${file}" 2>/dev/null; then
                echo "${file}"
                found_any=true
                break
            fi
        done
    done
}

scan_for_todos() {
    local files="$1"
    local found=0
    echo "${files}" | while IFS= read -r file; do
        [[ -z "${file}" ]] && continue
        [[ ! -f "${file}" ]] && continue
        local todos
        todos=$(grep -c "TODO\|FIXME\|HACK\|XXX" "${file}" 2>/dev/null || echo "0")
        found=$((found + todos))
    done
    echo "${found}"
}

# ============================================================================
# Git utility
# ============================================================================
get_commit_msg_file() {
    local msg_file="${1:-}"
    if [[ -z "${msg_file}" ]]; then
        msg_file=".git/COMMIT_EDITMSG"
    fi
    echo "${msg_file}"
}

get_commit_message() {
    local msg_file
    msg_file=$(get_commit_msg_file "$1")
    if [[ -f "${msg_file}" ]]; then
        head -n 1 "${msg_file}" 2>/dev/null || echo ""
    else
        echo ""
    fi
}

# ============================================================================
# Final summary
# ============================================================================
show_summary() {
    local hook_name="$1"
    local elapsed="${2:-0}"
    local hook_lower
    hook_lower=$(echo "${hook_name}" | tr '[:upper:]' '[:lower:]')

    echo ""
    if [[ "${PASS}" == "true" ]]; then
        echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}${BOLD}║     ✅  ALL CHECKS PASSED - ${hook_name} ALLOWED            ║${NC}"
        echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "  ${GREEN}${hook_name} is ready to proceed!${NC}"
        if (( elapsed > 0 )); then
            echo -e "  ${DIM}Completed in ${elapsed}s${NC}"
        fi
        echo ""
    else
        echo -e "${RED}${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${RED}${BOLD}║     ❌  CHECKS FAILED - ${hook_name} BLOCKED                ║${NC}"
        echo -e "${RED}${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "  ${RED}Please fix the issues above and try again.${NC}"
        echo ""
        echo -e "  ${YELLOW}To bypass checks temporarily (not recommended):${NC}"
        echo -e "    git ${hook_lower} --no-verify"
        echo ""
        exit 1
    fi
}

# Self-validation
self_validate() {
    local hook_name="$1"
    local errors=0

    if [[ ! -d "${PROJECT_ROOT}" ]]; then
        echo "  ${RED}✗${NC} Cannot access project root: ${PROJECT_ROOT}"
        errors=$((errors + 1))
    fi

    if ! git rev-parse --git-dir &>/dev/null; then
        echo "  ${RED}✗${NC} Not in a git repository"
        errors=$((errors + 1))
    fi

    if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
        echo "  ${YELLOW}⚠${NC} This script should be sourced, not executed directly"
    fi

    if [[ -n "${_HOOK_RUNNING:-}" ]]; then
        echo "  ${RED}✗${NC} Circular hook execution detected (${_HOOK_RUNNING})"
        exit 1
    fi
    export _HOOK_RUNNING="${hook_name}"

    if (( errors > 0 )); then
        echo "  ${RED}Hook self-validation failed${NC}"
        exit 1
    fi

    return 0
}