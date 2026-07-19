const features = [
    {
        title: 'Monorepo shell',
        description: 'A well-separated structure for web, API, and shared packages.',
    },
    {
        title: 'Type-safe contracts',
        description: 'Shared models and API payloads that stay consistent across layers.',
    },
    {
        title: 'Auth and billing scaffolding',
        description: 'Ready-made routes and plans for expanding into SaaS workflows.',
    },
];

export default function App() {
    return (
        <main className="app-shell">
            <section className="hero">
                <p className="eyebrow">React Starter Kit inspired monorepo</p>
                <h1>Build your SaaS product with a unified web + API foundation.</h1>
                <p className="summary">
                    This workspace now includes an app shell, backend service, shared contracts,
                    developer docs, and deployment-ready scaffolding.
                </p>
            </section>

            <section className="features" aria-label="starter kit highlights">
                {features.map((feature) => (
                    <article key={feature.title} className="card">
                        <h2>{feature.title}</h2>
                        <p>{feature.description}</p>
                    </article>
                ))}
            </section>
        </main>
    );
}
