'use client';

import SectionTitle from '@/components/section-title';
import { ChevronDownIcon } from 'lucide-react';
import { useState } from 'react';

export default function FaqSection() {
    const [isOpen, setIsOpen] = useState(false);
    const data = [
        {
            question: 'What is TalentPilot and how does it help my organization?',
            answer: 'TalentPilot is an AI-powered HR orchestration agent powered by IBM WatsonX. It automates recruitment, talent management, performance tracking, and strategic HR operations. It uses your organizational data to provide intelligent insights and recommendations.',
        },
        {
            question: 'What data sources does TalentPilot use?',
            answer: 'TalentPilot integrates with your recruitment database, employee records, training and development data, and employee engagement surveys. This allows us to provide comprehensive insights across your entire talent lifecycle.',
        },
        {
            question: 'How does TalentPilot improve recruitment efficiency?',
            answer: 'TalentPilot analyzes your recruitment data to identify trends, predict successful hires, optimize hiring pipelines, and accelerate time-to-hire. It also helps you identify skill gaps and compensation competitiveness.',
        },
        {
            question: 'Can TalentPilot help with employee engagement and retention?',
            answer: 'Yes. TalentPilot analyzes employee engagement survey data, identifies satisfaction trends, and provides actionable recommendations to improve workplace culture, work-life balance, and retention.',
        },
        {
            question: 'Is my data secure and private with TalentPilot?',
            answer: 'Absolutely. TalentPilot follows enterprise security standards and is powered by IBM WatsonX, which complies with major data privacy regulations. Your data is encrypted and never shared without authorization.',
        },
        {
            question: 'How do I get started with TalentPilot?',
            answer: 'Sign up for the Starter plan (free) to get immediate access to the TalentPilot chat interface. You can start asking questions and gaining HR insights right away. Upgrade anytime for advanced features.',
        },
    ];

    return (
        <section className='mt-32'>
            <SectionTitle title="Frequently Asked Questions" description="Everything you need to know about TalentPilot and how it transforms your HR operations." />
            <div className='mx-auto mt-12 space-y-4 w-full max-w-xl'>
                {data.map((item, index) => (
                    <div key={index} className='flex flex-col glass rounded-md'>
                        <h3 className='flex cursor-pointer hover:bg-white/10 transition items-start justify-between gap-4 p-4 font-medium' onClick={() => setIsOpen(isOpen === index ? null : index)}>
                            {item.question}
                            <ChevronDownIcon className={`size-5 transition-all shrink-0 duration-400 ${isOpen === index ? 'rotate-180' : ''}`} />
                        </h3>
                        <p className={`px-4 text-sm/6 transition-all duration-400 overflow-hidden ${isOpen === index ? 'pt-2 pb-4 max-h-80' : 'max-h-0'}`}>{item.answer}</p>
                    </div>
                ))}
            </div>
        </section>
    );
}