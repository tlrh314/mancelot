import { h, Component } from 'preact';
import style from './style';
import Productitem from "../productitem";
import FilterMenu from "../filtermenu";
// todo: doorgeven als prop
import products from "../../data/products.json";

const randomOrder = products.sort((a, b) => Math.random() * 2 - 1);

const colors = {
    "Green" : "#53b748",
    "Brown" : "#7f471d",
    "Purple" : "#5d318c",
    "Denim" : "#4e7ca5",
    "Blue" : "#1babea",
    "Beige" : "#e9d8ac",
    "White" : "#efefef",
    "Grey" : "#a8a8a8",
    "Black" : "#000000",
    "Yellow" : "#fdd300",
    "Orange" : "#f58a1f",
    "Red" : "#ba1c1c",
    "Pink" : "#f28bb9"
};

const colorFilterOptions = Object.keys(colors);

export default class FilteredExplorer extends Component {

    tileWidth = 20;
    tileMargin = 5;

    state = {
        visibleColors : []
    };

    renderItem = (item, i) => {
        const { columnCount, tileWidth, tileMargin } = this;

        const tileSpace = (tileWidth + tileMargin);

        const y = Math.floor(i / columnCount);
        const x = i % columnCount;

        return (
            <Productitem
                key={item.id}
                x={x * tileSpace + y % 2 * tileSpace / 2}
                y={y * tileSpace}
                color={colors[ item.color ]}
            />
        );
    };

    updateColorFilter = e => {
        const selectedOptions = Array.apply(null, e.target.selectedOptions);
        this.setState({
                          visibleColors : selectedOptions.map(
                              option => option.value)
                      });
    };

    render() {
        const { visibleColors } = this.state;
        const filteredProducts = products.filter(
            product => visibleColors.includes(product.color));

        this.columnCount = Math.ceil(Math.sqrt(filteredProducts.length));

        return (
            <div className="app">
                <div style={{ width : 900, height : 800 }}>
                    {filteredProducts.map(this.renderItem)}
                </div>
                <FilterMenu
                    colorFilterOptions={colorFilterOptions}
                    onUpdateFilter={this.updateColorFilter}
                />
            </div>
        );
    }

}
