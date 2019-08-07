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
              <div class="btn_back_container"><button class="btn_back" onClick={ e => alert("navigate back to home") }></button></div>
              <h1>Wil je kleur bekennen?</h1>
              <h2>Je kunt meerdere kleuren kiezen</h2>
                {/*<FilteredExplorer />*/}
                <Grid
                    columnCount={3}
                    elementCount={12}
                    onClick={i => console.log(i)}
                />
                <div class="footer_bar"><button class="btn_full" onClick={ e => alert("nice animation starts here!") }>Verder</button></div>
            </div>

        );
    }
}
