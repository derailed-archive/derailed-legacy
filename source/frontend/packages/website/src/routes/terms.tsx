import React from 'react';
import TermsMD from './terms.mdx';
import { components } from '../mdx_components';
import Header from '@derailed/web-components/Header';


export default function Terms() {
    return (
        <div className="relative bg-[#202024] h-max min-h-screen mb:pl-5 mb:pr-5">
            <Header />
            <TermsMD components={components} />
        </div>
    )
}
