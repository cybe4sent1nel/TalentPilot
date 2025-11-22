'use client';

import { useEffect } from 'react';

export default function ChatScrollHandler() {
    useEffect(() => {
        // Disable Lenis for this route since we have custom scroll handling
        const html = document.documentElement;
        
        // Store original styles
        const originalStyle = html.getAttribute('style');
        
        // Try to disable Lenis if it's active
        if (window.lenis) {
            window.lenis.destroy();
        }

        return () => {
            // Restore on unmount
            if (originalStyle) {
                html.setAttribute('style', originalStyle);
            }
        };
    }, []);

    return null;
}
