class Dictionary {

    constructor(data = {}) {
        this.data = data;
    }

    add(key, value) {
        this.data[ key ] = value;
    }

    remove(key) {
        delete this.data[ key ];
    }

    contains(key) {
        return this.data[ key ] !== undefined;
    }

    get(key) {
        return (this.contains(key)) ? this.data[ key ] : this.data.default;
    }

    get default() {
        return this.data.default;
    }

    set default(value) {
        this.data.default = value;
    }

}

export default Dictionary;