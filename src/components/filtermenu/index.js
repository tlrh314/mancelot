import { h, Component } from 'preact';
import style from './style';

export default class FilterMenu extends Component {

    static defaultProps = {
        color : "#FF0000"
    };

    getStyle() {
        const { x, y } = this.props;

        return {
            left : x,
            top : y
        };
    }

    render() {
        const {colorFilterOptions, onUpdateFilter} = this.props;

        return (
            <div class={style.filterMenu}>
                <select
                    name="color"
                    onChange={onUpdateFilter}
                    multiple
                >
                    {colorFilterOptions.map((option, i) => (
                        <option
                            value={option}
                            key={i}
                        >{option}</option>
                    ))}
                </select>
            </div>
        );
    }
}