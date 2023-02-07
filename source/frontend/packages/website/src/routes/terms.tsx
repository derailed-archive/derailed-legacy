import React from 'react';
import TermsMD from './terms.mdx';
import { components } from '../mdx_components';
import Header from '@derailed/web-components/Header';


export default function Terms() {
    return (
        <div className="relative bg-[#202024] h-max min-h-screen">
            <Header />
            <TermsMD components={components} />
        </div>
    )
}
