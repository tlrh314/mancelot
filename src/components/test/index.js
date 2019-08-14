import { h, Component } from 'preact';
import style from './style';

export default class Test extends Component {

    static defaultProps = {
        color : "#FF0000"
    };

    render() {
        return (
            <div class="test">
                TESTJE
            </div>
        );
    }
}
