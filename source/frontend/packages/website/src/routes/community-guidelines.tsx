import React from 'react';
import CommunityGuidelinesMD from './community-guidelines.mdx';
import { components } from '../mdx_components';
import Header from '@derailed/web-components/Header';


export default function CommunityGuidelines() {
    return (
        <div className="relative bg-[#202024] h-max min-h-screen mb:pl-5 mb:pr-5">
            <Header />
            <CommunityGuidelinesMD components={components} />
        </div>
    )
}
