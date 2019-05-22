import { h, Component } from 'preact';
import style from './style';
import { createArray } from "../../utils/collection/array.utils";

export default class Grid extends Component {

    static defaultProps = {
        columnCount : 3,
        elementCount : 3,
        onClick : () => {
        }
    };

    // todo: Element Class doorgeven als prop
    renderElement = (element, i) => (
        <div onClick={() => this.props.onClick(i)}>{i + 1}</div>
    );

    render() {
        const { columnCount, elementCount } = this.props;

        const styling = {
            gridTemplateColumns : `repeat(${columnCount}, 1fr)`
        };

        return (
            <div
                className={style.grid}
                style={styling}
            >
                {createArray(elementCount).map(this.renderElement)}
            </div>
        );
    }
}