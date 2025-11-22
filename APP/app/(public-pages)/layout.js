import Footer from '@/components/footer';
import Navbar from '@/components/navbar';

export const metadata = {
    title: 'TalentPilot - HR Intelligence Agent',
    description: 'AI-powered HR Intelligence Agent powered by IBM WatsonX. Automate recruitment, talent management, and HR operations.',
    appleWebApp: {
        title: 'TalentPilot - HR Intelligence Agent',
    },
};

export default function Layout({ children }) {
    return (
        <>
            <Navbar />
            <div className="fixed inset-0 overflow-hidden -z-20 pointer-events-none">
                <div className="absolute rounded-full top-80 left-1/3 -translate-x-1/2 size-130 bg-[#D10A8A] blur-[100px]" />
                <div className="absolute rounded-full top-80 -right-20 -translate-x-1/2 size-130 bg-[#2E08CF] blur-[100px]" />
                <div className="absolute rounded-full top-0 left-1/2 -translate-x-1/2 size-130 bg-[#F26A06] blur-[100px]" />
            </div>
            {children}
            <Footer />
        </>
    );
}
