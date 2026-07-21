#!/bin/bash
# ============================================================================
# Git Hooks Installation Script for Python Starter Kit
# Installs .githooks/ hooks and configures Git to use them
# ============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
HOOKS_DIR="${PROJECT_ROOT}/.githooks"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

echo -e "\n${CYAN}${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}║     🔧 Python Starter Kit - Git Hooks Installer             ║${NC}"
echo -e "${CYAN}${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check we're in the project root
if [[ ! -d "${HOOKS_DIR}" ]]; then
    echo -e "  ${RED}✗${NC} Hooks directory not found: ${HOOKS_DIR}"
    echo -e "  ${RED}✗${NC} Run this script from the project root."
    exit 1
fi

# Check git repo
if ! git rev-parse --git-dir &>/dev/null; then
    echo -e "  ${RED}✗${NC} Not in a git repository."
    exit 1
fi

# Configure Git to use our hooks directory
echo -e "  ${CYAN}ℹ${NC} Setting core.hooksPath to ${HOOKS_DIR}"
git config core.hooksPath "${HOOKS_DIR}"

# Make hooks executable
echo -e "  ${CYAN}ℹ${NC} Making hooks executable..."
chmod +x "${HOOKS_DIR}/pre-commit"
chmod +x "${HOOKS_DIR}/commit-msg"
chmod +x "${HOOKS_DIR}/pre-push"
chmod +x "${HOOKS_DIR}/lib/shared.sh"

echo ""
echo -e "  ${GREEN}✓${NC} Hooks installed successfully!"
echo ""
echo -e "  ${BOLD}Installed hooks:${NC}"
echo -e "    ${GREEN}pre-commit${NC}   - Branch protection, file validation, secret scanning,"
echo -e "                     formatting, linting, type checking, tests"
echo -e "    ${GREEN}commit-msg${NC}   - Conventional commits validation"
echo -e "    ${GREEN}pre-push${NC}     - Branch protection, full tests, quality checks,"
echo -e "                     commit history inspection"
echo ""
echo -e "  ${YELLOW}To bypass temporarily: git commit --no-verify${NC}"
echo -e "  ${DIM}Hooks location: ${HOOKS_DIR}${NC}"
echo -e "  ${DIM}To verify: git config --get core.hooksPath${NC}"
echo ""