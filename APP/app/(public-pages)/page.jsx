import CallToAction from '@/sections/call-to-action';
import FaqSection from '@/sections/faq-section';
import Features from '@/sections/features';
import HeroSection from '@/sections/hero-section';
import PricingPlans from '@/sections/pricing-plans';
import Testimonials from '@/sections/testimonials';
import TrustedCompanies from '@/sections/trusted-companies';
import WorkflowSteps from '@/sections/workflow-steps';

export default function Page() {
    return (
        <main className='px-4'>
            <HeroSection />
            <TrustedCompanies />
            <Features />
            <WorkflowSteps />
            <Testimonials />
            <FaqSection />
            <PricingPlans />
            <CallToAction />
        </main>
    );
}
