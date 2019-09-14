import { h, Component } from 'preact';
import { Router } from 'preact-router';

import Firstuse from '../routes/firstuse';
import Home from '../routes/home';
import ColourSelection from '../routes/colourselection';
import Overview from '../routes/overview';
import About from '../routes/about';

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
                <Router onChange={this.handleRoute}>
                    <Home default />
                    <Firstuse path="/firstuse/" />
                    <ColourSelection path="/colourselection/" />
                    <Overview path="/overview/:colour" />
                    <About path="/about/" />
                </Router>
            </div>
        );
    }
}
