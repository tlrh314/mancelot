import React from 'react';

class FilterMenu extends React.Component {

    render() {
        const {colorFilterOptions, onUpdateFilter} = this.props;

        return (
            <div className="filterMenu">
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

export default FilterMenu;