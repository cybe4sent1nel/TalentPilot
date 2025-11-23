'use client';

import { SendIcon, MenuIcon, XIcon, SparklesIcon } from 'lucide-react';
import Link from 'next/link';
import { useEffect, useRef, useState } from 'react';
import { sendMessage } from '@/lib/openrouter';
import { samplePrompts } from '@/lib/samplePrompts';
import {
  searchApplicant,
  searchApplicantsByJobTitle,
  getCommonJobTitles,
  getApplicantsByStatus,
  searchEmployee,
  getEmployeesByDepartment,
  getTrainingByEmployee,
  getKnowledgeBaseSummary,
} from '@/lib/knowledgeBaseHelper';

export default function ChatPage() {
    const [messages, setMessages] = useState([
        {
            id: 1,
            text: "Hello! I'm TalentPilot, your HR Intelligence Agent powered by IBM WatsonX. I have access to your organization's recruitment, employee, training, and engagement data. How can I help you today?",
            sender: 'bot',
            timestamp: new Date(),
        },
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
    const [showSamples, setShowSamples] = useState(true);
    const messagesEndRef = useRef(null);
    const messagesContainerRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Smooth wheel scrolling for the messages container using Lenis-like effect
    useEffect(() => {
        const container = messagesContainerRef.current;
        if (!container) return;

        let scrollVelocity = 0;
        let isAnimating = false;
        const friction = 0.94;
        const acceleration = 0.08;
        const maxVelocity = 50;

        const handleWheel = (e) => {
            e.preventDefault();
            
            // Accumulate velocity
            scrollVelocity += e.deltaY * acceleration;
            
            // Clamp velocity
            scrollVelocity = Math.max(Math.min(scrollVelocity, maxVelocity), -maxVelocity);
            
            // Start animation if not already running
            if (!isAnimating) {
                isAnimating = true;
                
                const animate = () => {
                    if (Math.abs(scrollVelocity) > 0.5) {
                        container.scrollTop += scrollVelocity;
                        scrollVelocity *= friction;
                        requestAnimationFrame(animate);
                    } else {
                        isAnimating = false;
                        scrollVelocity = 0;
                    }
                };
                
                requestAnimationFrame(animate);
            }
        };

        container.addEventListener('wheel', handleWheel, { passive: false });
        
        return () => {
            container.removeEventListener('wheel', handleWheel);
        };
    }, []);

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = {
            id: messages.length + 1,
            text: input,
            sender: 'user',
            timestamp: new Date(),
        };

        setMessages((prev) => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);
        setShowSamples(false);

        try {
            // Check if the query requires knowledge base lookup
            let kbContext = '';
            const inputLower = input.toLowerCase();

            // Pattern matching for knowledge base queries
            if (
                inputLower.includes('applicant') ||
                inputLower.includes('candidate') ||
                inputLower.includes('recruiting') ||
                inputLower.includes('application status')
            ) {
                try {
                    // Try to extract name for applicant search
                    const nameMatch = input.match(/(\w+)\s+(\w+)/);
                    if (nameMatch && !inputLower.includes('common') && !inputLower.includes('trend')) {
                        const firstName = nameMatch[1];
                        const lastName = nameMatch[2];
                        const applicantData = await searchApplicant(firstName, lastName);
                        if (applicantData) {
                            kbContext = `\n\n[From Knowledge Base - Applicant Record]\nApplicant Name: ${applicantData['First Name']} ${applicantData['Last Name']}\nApplicant ID: ${applicantData['Applicant ID']}\nJob Title: ${applicantData['Job Title']}\nStatus: ${applicantData['Status']}\nDesired Salary: ${applicantData['Desired Salary']}\nYears of Experience: ${applicantData['Years of Experience']}\nEducation Level: ${applicantData['Education Level']}\nApplication Date: ${applicantData['Application Date']}`;
                        }
                    }

                    // Check for job title trend queries
                    if (inputLower.includes('common') && inputLower.includes('job')) {
                        const jobTitles = await getCommonJobTitles();
                        const topTitles = jobTitles.slice(0, 5)
                            .map((t) => `${t.title} (${t.count})`)
                            .join(', ');
                        kbContext = `\n\n[From Knowledge Base - Top Job Titles]\n${topTitles}`;
                    }
                } catch (kbError) {
                    console.warn('Knowledge base query failed:', kbError);
                }
            }

            if (
                inputLower.includes('employee') ||
                inputLower.includes('staff') ||
                inputLower.includes('team member')
            ) {
                try {
                    const nameMatch = input.match(/(\w+)\s+(\w+)/);
                    if (nameMatch && !inputLower.includes('training') && !inputLower.includes('department')) {
                        const firstName = nameMatch[1];
                        const lastName = nameMatch[2];
                        const employeeData = await searchEmployee(firstName, lastName);
                        if (employeeData) {
                            kbContext = `\n\n[From Knowledge Base - Employee Record]\nEmployee Name: ${employeeData['FirstName']} ${employeeData['LastName']}\nEmployee ID: ${employeeData['EmpID']}\nTitle: ${employeeData['Title']}\nDepartment: ${employeeData['DepartmentType']}\nStatus: ${employeeData['EmployeeStatus']}\nPerformance Score: ${employeeData['Performance Score']}`;
                        }
                    }
                } catch (kbError) {
                    console.warn('Knowledge base query failed:', kbError);
                }
            }

            const apiMessages = messages
                .filter(m => m.id > 1)
                .map(m => ({
                    role: m.sender === 'user' ? 'user' : 'assistant',
                    content: m.text,
                }));
            
            apiMessages.push({
                role: 'user',
                content: input + kbContext,
            });

            const response = await sendMessage(apiMessages);

            const botMessage = {
                id: messages.length + 2,
                text: response,
                sender: 'bot',
                timestamp: new Date(),
            };
            setMessages((prev) => [...prev, botMessage]);
        } catch (error) {
            const errorMessage = {
                id: messages.length + 2,
                text: `Error: ${error.message}. Please make sure your OpenRouter API key is configured in environment variables.`,
                sender: 'bot',
                timestamp: new Date(),
            };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSamplePromptClick = (prompt) => {
        setInput(prompt);
    };

    return (
        <div className='flex h-screen text-white relative overflow-hidden'>

            {/* Sidebar */}
            <div
                className={`border-r border-white/10 bg-gradient-to-b from-white/5 to-white/0 backdrop-blur-md transition-all duration-300 ${
                    isSidebarOpen ? 'w-64' : 'w-0'
                } overflow-hidden z-40`}
            >
                <div className='flex flex-col h-full p-4'>
                    <Link
                        href='/'
                        className='mb-6 text-xl font-bold hover:text-gray-300 transition'
                    >
                        TalentPilot
                    </Link>

                    <button className='btn glass w-full py-2.5 mb-6'>
                        + New Chat
                    </button>

                    <div className='flex-1 overflow-y-auto space-y-2'>
                        <p className='text-xs text-gray-500 px-1 py-2'>Recent Conversations</p>
                        <div className='p-3 rounded-lg bg-white/5 hover:bg-white/10 transition cursor-pointer text-sm truncate'>
                            Recruitment Analysis
                        </div>
                        <div className='p-3 rounded-lg bg-white/5 hover:bg-white/10 transition cursor-pointer text-sm truncate'>
                            Employee Engagement Trends
                        </div>
                        <div className='p-3 rounded-lg bg-white/5 hover:bg-white/10 transition cursor-pointer text-sm truncate'>
                            Training Program ROI
                        </div>
                    </div>

                    <div className='border-t border-white/10 pt-4 mt-4 text-xs text-gray-400'>
                        <p className='font-semibold mb-2'>Powered by IBM WatsonX</p>
                        <p>Designed and developed by Fahad Khan</p>
                    </div>
                </div>
            </div>

            {/* Main Chat Area */}
            <div className='flex flex-1 flex-col relative z-30'>
                {/* Header */}
                <header className='border-b border-white/10 bg-gradient-to-b from-white/5 to-transparent backdrop-blur-md px-6 py-4 flex items-center justify-between'>
                    <button
                        onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                        className='transition hover:text-gray-300'
                    >
                        {isSidebarOpen ? (
                            <XIcon className='size-6' />
                        ) : (
                            <MenuIcon className='size-6' />
                        )}
                    </button>

                    <h1 className='text-lg font-semibold flex items-center gap-2'>
                        <SparklesIcon className='size-5' />
                        TalentPilot Chat
                    </h1>

                    <Link
                        href='/'
                        className='text-sm transition hover:text-gray-300'
                    >
                        Back to Home
                    </Link>
                </header>

                {/* Messages Container */}
                <div className='flex-1 flex flex-col overflow-hidden bg-black/30'>
                    {/* Messages Area - Scrollable */}
                    <div 
                        ref={messagesContainerRef}
                        className='flex-1 overflow-y-auto px-6 py-8 space-y-6'
                    >
                    {messages.map((message) => (
                        <div
                            key={message.id}
                            className={`flex ${
                                message.sender === 'user'
                                    ? 'justify-end'
                                    : 'justify-start'
                            }`}
                        >
                            <div
                                className={`max-w-2xl rounded-2xl px-6 py-4 ${
                                    message.sender === 'user'
                                        ? 'bg-white/10 border border-white/20 text-white'
                                        : 'bg-white/5 border border-white/20 text-gray-100'
                                }`}
                            >
                                <p className='text-sm/relaxed whitespace-pre-wrap'>{message.text}</p>
                                <p className='mt-2 text-xs text-gray-500'>
                                    {message.timestamp.toLocaleTimeString()}
                                </p>
                            </div>
                        </div>
                    ))}

                    {isLoading && (
                        <div className='flex justify-start'>
                            <div className='rounded-2xl bg-white/5 border border-white/20 px-6 py-4'>
                                <div className='flex gap-2'>
                                    <div className='size-2 rounded-full bg-gray-400 animate-bounce'></div>
                                    <div
                                        className='size-2 rounded-full bg-gray-400 animate-bounce'
                                        style={{ animationDelay: '0.2s' }}
                                    ></div>
                                    <div
                                        className='size-2 rounded-full bg-gray-400 animate-bounce'
                                        style={{ animationDelay: '0.4s' }}
                                    ></div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Sample Prompts - Show when no messages beyond greeting */}
                    {showSamples && messages.length === 1 && (
                        <div className='mt-8'>
                            <p className='text-sm text-gray-400 mb-4'>Example conversations you can try:</p>
                            <div className='grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl'>
                                {samplePrompts.slice(0, 2).map((category, idx) => (
                                    <div key={idx}>
                                        <p className='text-xs font-semibold text-gray-300 mb-2'>{category.category}</p>
                                        <div className='space-y-2'>
                                            {category.prompts.slice(0, 2).map((prompt, pidx) => (
                                                <button
                                                    key={pidx}
                                                    onClick={() => handleSamplePromptClick(prompt)}
                                                    className='w-full text-left text-xs bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg p-3 transition'
                                                >
                                                    {prompt}
                                                </button>
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                    </div>
                </div>

                {/* Input Area */}
                <div className='border-t border-white/10 bg-gradient-to-t from-white/5 to-transparent backdrop-blur-md px-6 py-6 flex-shrink-0'>
                    <form onSubmit={handleSendMessage} className='flex gap-3 mb-4'>
                        <input
                            type='text'
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder='Ask about recruitment, talent management, or HR operations...'
                            className='flex-1 rounded-full bg-white/10 border border-white/20 px-6 py-3.5 text-sm placeholder-gray-400 focus:border-white/40 focus:outline-none transition'
                            disabled={isLoading}
                        />
                        <button
                            type='submit'
                            disabled={isLoading || !input.trim()}
                            className='btn glass !rounded-full p-3.5 flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed'
                        >
                            <SendIcon className='size-5' />
                        </button>
                    </form>

                    <p className='text-xs text-gray-500 text-center'>
                        TalentPilot powered by IBM WatsonX | Designed and developed by Fahad Khan
                    </p>
                </div>
            </div>
        </div>
    );
}
