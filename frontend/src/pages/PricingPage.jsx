/**
 * Pricing Page - Displays subscription plans and allows admins to manage billing
 * 
 * Features:
 * - Shows Clerk's pricing table for organization subscriptions
 * - Only organization admins can view and manage subscriptions
 * - Non-admins see a message to contact their admin
 * - Users without an organization are prompted to create one
 */

import {useOrganization} from "@clerk/clerk-react";
import {PricingTable, CreateOrganization} from "@clerk/clerk-react";

function PricingPage() {
    // Get current organization and user's membership role
    const {organization, membership} = useOrganization()
    const isAdmin = membership?.role === "org:admin"

    // If user is not in an organization, show create organization prompt
    if (!organization) {
        return <div className={"pricing-container"}>
            <div className={"no-org-container"}>
                <h1 className={"no-org-title"}>View Pricing</h1>
                <p className={"no-org-text"}>
                    Create or join an organization to view pricing plans.
                </p>
                <CreateOrganization afterCreateOrganizationUrl={"/pricing"}/>
            </div>
        </div>
    }

    // User has an organization - show pricing page
    return <div className={"pricing-container"}>
        <div className={"pricing-header"}>
            <h1 className={"pricing-title"}>Simple, Transparent Pricing</h1>
            <p>
                Start free with up to 2 members, Upgrade to pro for unlimited members
            </p>
        </div>

        {/* Only admins can manage subscriptions, others see a message */}
        {!isAdmin ? (
            <p className={"text-muted pricing-admin-note"}>
                Contact your organizations admin for manage the subscription.
            </p>
        ) : (
            // Clerk's pricing table component handles the subscription flow
            <PricingTable for={"organization"} />
        )}
    </div>
}

export default PricingPage