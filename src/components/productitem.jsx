import React from 'react';

class Productitem extends React.Component {

    constructor(props) {
        super(props);
    }

    getStyle() {
        const { x, y } = this.props;

        return {
            left : x,
            top : y
        };
    }

    render() {
        const style = this.getStyle();
        const { color } = this.props;

        return (
            <div className="productitem" style={style}>
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 448 448"
                    fill={color}
                >
                    <path
                        d="M364 200l84-20 -20-99.8c0-6.5-4-12.4-10.1-14.8l-122-53c-0.8-0.3-1.6-0.4-2.5-0.4h-0.3c-8.8 30.3-36.6 52-69.1 52 -32.5 0-60.4-21.7-69.1-52h-0.3c-0.8 0-1.6 0.1-2.3 0.3L29.6 65.6c-5.9 2.5-9.7 8.3-9.6 14.6L0 180l84 20 11-38h5L90 448h268l-10-286h5L364 200z" />
                </svg>
            </div>
        );
    }
}

Productitem.defaultProps = {
    color: "#FF0000"
};

export default Productitem;