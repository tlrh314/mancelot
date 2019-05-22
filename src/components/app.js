import { h, Component } from 'preact';
import Grid from './grid';
import products from "../data/products.json";
import FilteredExplorer from "./filteredexplorer";

export default class App extends Component {

    state = {
        showDetail : false,
        currentRoute : ''
    };

    routes = {};

    handleRoute = e => {
        const currentRoute = e.url;
        const showDetail = currentRoute !== '/';
        const newState = { showDetail, currentRoute };
        if ( showDetail ){
            newState.currentPage = this.routes[ currentRoute ];
        }
        this.setState(newState);
    };

    render() {
        return (
            <div id="app">
                {/*<FilteredExplorer />*/}
                <Grid
                    columnCount={3}
                    elementCount={9}
                    onClick={i => console.log(i)}
                />
            </div>
        );
    }
}
