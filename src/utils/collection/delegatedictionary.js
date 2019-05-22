import Dictionary from './dictionary';

class DelegateDictionary extends Dictionary {

    constructor(data = {}) {
        super(data);
    }

    invoke(key, ...params) {
        this.triggerDelegate('always', params);
        return this.triggerDelegate(key, params);
    }

    triggerDelegate(key, params) {
        const delegate = this.get(key);
        if ( !delegate || typeof delegate != 'function' ){
            return false;
        }
        delegate(...params);
        return true;
    }

}

export default DelegateDictionary;