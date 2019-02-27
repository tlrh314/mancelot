import React from 'react';
import Productitem from "./components/productitem";
import PinchToZoom from 'react-pinch-and-zoom';
import products from "./products.json";

const randomOrder = products.sort((a, b) => Math.random() * 2 - 1);

const colors = {
    "Green"      : "#53b748",
    "Brown"      : "#7f471d",
    "Purple"     : "#5d318c",
    "Denim"      : "#4e7ca5",
    "Blue"       : "#1babea",
    "Beige"      : "#e9d8ac",
    "White"      : "#efefef",
    "Grey"       : "#a8a8a8",
    "Black"      : "#000000",
    "Yellow"     : "#fdd300",
    "Orange"     : "#f58a1f",
    "Red"        : "#ba1c1c",
    "Pink"       : "#f28bb9"
};

class App extends React.Component {

    constructor(props) {
        super(props);

        this.columnCount = 35;
        this.tileWidth = 20;
        this.tileMargin = 5;
    }

    renderItem = (item, i) => {
        const { columnCount, tileWidth, tileMargin } = this;

        const tileSpace = (tileWidth + tileMargin);

        const y = Math.floor(i / columnCount);
        const x = i % columnCount;

        return (
            <Productitem
                key={i}
                x={x * tileSpace + y % 2 * tileSpace / 2}
                y={y * tileSpace}
                color={colors[item.color]}
            />
        );
    };

    render() {
        return (
            <div className="app">
                <div className="menu">
                    <select name="color" multiple>
                        <option value="green">Volvo</option>
                    </select>
                </div>
                <PinchToZoom maxZoomScale={8.0}>
                    <div style={{ width : 900, height : 800 }}>
                        {products.map(this.renderItem)}
                    </div>
                </PinchToZoom>
            </div>
        );
    }

}

export default App;