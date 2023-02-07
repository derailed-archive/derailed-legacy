import Header from '@derailed/web-components/Header';
import Intro from '@derailed/web-components/Intro';
import Features from '@derailed/web-components/Features';
import Footer from '@derailed/web-components/Footer';


function Root() {
  return (
    <div className="relative h-max min-h-screen">
      <div className='bg-[#202024] pb-40 mb:pl-5 mb:pr-5'>
        <Header />
        <Intro />
      </div>
      <Features />
      <Footer />
    </div>
  )
}

export default Root
