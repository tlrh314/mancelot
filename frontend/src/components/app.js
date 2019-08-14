import { h, Component } from 'preact';
import { Router } from 'preact-router';

import Home from '../routes/home';
import ColourSelection from '../routes/colourselection';
import Overview from '../routes/overview';

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
                    <ColourSelection path="/colourselection/" />
                    <Overview path="/overview/:colour" />
                </Router>
            </div>
        );
    }
}
