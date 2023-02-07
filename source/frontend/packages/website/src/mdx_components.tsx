// @ts-nocheck

export let components = {
    a: props => <a className="text-lg pb-3 max-w-3xl m-auto text-justify text-[#807ef2]" {...props} />,
    h1: props => <h1 className="text-3xl font-bold text-white pb-10 text-center m-auto" {...props} />,
    h2: props => <h2 className="text-2xl font-semibold text-center text-white pb-7 pt-4" {...props} />,
    h3: props => <h3 className="text-xl font-semibold text-center text-white pb-7 pt-4" {...props} />,
    p: props => <p className="text-lg text-white pb-3 max-w-3xl m-auto text-justify" {...props} />,
    br: () => <br className="pb-5" />,
    ul: props => <ul className="pb-3 justify-items-center" {...props} />,
    li: props => {
        if (typeof props.children === "string") {
            props = {children: '• ' + props.children}
        }

        return <li className="text-lg text-center text-white m-auto pb-4" {...props} />
    }
};
