import { h, Component } from 'preact';
import style from './style';
import { createArray } from '../../utils/collection/array.utils';
import classNames from 'classnames';

export default class Grid extends Component {

    static defaultProps = {
        columnCount : 4,
        elementCount : 4,
        selectedElements : [],
        onClick : () => {
        }
    };

    // todo: Element Class doorgeven als prop
    renderElement = (element, i) => {
        const className = classNames({
            ["color"+(i + 1)] : true,
            selected : this.props.selectedElements.includes(i)
        });
        return (
            <div class={className} onClick={() => this.props.onClick(i)}></div>
        );
    };

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
