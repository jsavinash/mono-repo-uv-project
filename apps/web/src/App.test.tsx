import { render, screen } from '@testing-library/react';
import App from './App';

describe('App', () => {
    it('renders the product headline', () => {
        render(<App />);
        expect(screen.getByText(/Build your SaaS product/i)).toBeInTheDocument();
    });
});
