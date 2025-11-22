import SectionTitle from "@/components/section-title";
import { CheckIcon, CrownIcon, RocketIcon, ZapIcon } from "lucide-react";

export default function PricingPlans() {
    const data = [
        {
            icon: RocketIcon,
            title: 'Starter',
            description: 'For individuals and small teams',
            price: '$0',
            buttonText: 'Get Started Free',
            features: [
                'Up to 5 recruitment workflows',
                'Basic talent orchestration',
                'Candidate tracking',
                'Email support',
                'Community access',
                'Standard integrations'
            ],
        },
        {
            icon: ZapIcon,
            title: 'Professional',
            description: 'For growing teams and startups',
            price: '$99',
            mostPopular: true,
            buttonText: 'Upgrade Now',
            features: [
                'Unlimited recruitment workflows',
                'Advanced talent orchestration',
                'Performance analytics & insights',
                'Priority support',
                'Custom integrations',
                'Team collaboration tools'
            ],
        },
        {
            icon: CrownIcon,
            title: 'Enterprise',
            description: 'For enterprises and agencies',
            price: '$499',
            buttonText: 'Contact Sales',
            features: [
                'Full HR orchestration suite',
                'Custom AI models & training',
                'Dedicated HR consultant',
                'Enterprise API access',
                '99.9% SLA guarantee',
                '24/7 dedicated support'
            ],
        },
    ];

    return (
        <section className="mt-32">
            <SectionTitle
                title="TalentPilot Pricing Plans"
                description="Choose the perfect plan for your HR orchestration needs. Scale from startup to enterprise."
            />

            <div className='mt-12 flex flex-wrap items-center justify-center gap-6'>
                {data.map((item, index) => (
                    <div key={index} className='group w-full max-w-80 glass p-6 rounded-xl hover:-translate-y-0.5 transition-all duration-300'>
                        <div className="flex items-center w-max ml-auto text-xs gap-2 glass rounded-full px-3 py-1">
                            <item.icon className='size-3.5' />
                            <span>{item.title}</span>
                        </div>
                        <h3 className='mt-4 text-2xl font-semibold'>
                            {item.price} <span className='text-sm font-normal'>/month</span>
                        </h3>
                        <p className='text-gray-200 mt-3'>{item.description}</p>
                        <button className={`mt-7 rounded-md w-full btn ${item.mostPopular ? 'bg-white text-gray-800' : 'glass'}`}>
                            {item.buttonText}
                        </button>
                        <div className='mt-6 flex flex-col'>
                            {item.features.map((feature, index) => (
                                <div key={index} className='flex items-center gap-2 py-2'>
                                    <div className='rounded-full glass border-0 p-1'>
                                        <CheckIcon className='size-3 text-white' strokeWidth={3} />
                                    </div>
                                    <p>{feature}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </section>
    );
}