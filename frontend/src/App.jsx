/**
 * App Component - Main application routing and layout
 * 
 * Defines all routes and handles authentication-based routing.
 * Uses Clerk for authentication and protects routes that require login.
 * 
 * Routes:
 * - / - Home page (public)
 * - /sign-in - Sign in page (public)
 * - /sign-up - Sign up page (public)
 * - /pricing - Pricing page (public)
 * - /dashboard - Dashboard (protected, requires authentication)
 */

import {Routes, Route} from 'react-router-dom'
import {SignedIn, SignedOut, RedirectToSignIn} from '@clerk/clerk-react'
import Layout from './components/Layout.jsx'
import HomePage from './pages/HomePage.jsx'
import SignInPage from './pages/SignInPage.jsx'
import SignUpPage from './pages/SignUpPage.jsx'
import PricingPage from './pages/PricingPage.jsx'
import DashboardPage from './pages/DashboardPage.jsx'

/**
 * ProtectedRoute - Wrapper component for routes that require authentication
 * 
 * Redirects unauthenticated users to the sign-in page.
 * Renders children only when user is signed in.
 */
function ProtectedRoute({children}) {
    return <>
        <SignedIn>
            {children}
        </SignedIn>
        <SignedOut>
            <RedirectToSignIn />
        </SignedOut>
    </>
}

function App() {
    return <Routes>
        <Route path="/" element={<Layout />}>
            <Route index element={<HomePage />} />
            <Route path={"sign-in/*"} element={<SignInPage />}/>
            <Route path={"sign-up/*"} element={<SignUpPage />}/>
            <Route path={"pricing"} element={<PricingPage />}/>
            <Route
                path={"dashboard"}
                element={
                <ProtectedRoute>
                    <DashboardPage />
                </ProtectedRoute>
                }
            />
        </Route>
    </Routes>
}

export default App
