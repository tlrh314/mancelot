/**
 * Push values in an array that is part of target object
 * @param collection
 * @param index
 * @param value
 */
const pushAt = (collection, index, value) => {
    if ( !collection ){
        return;
    }
    if ( !collection[ index ] ){
        collection[ index ] = [];
    }
    collection[ index ].push(value);
};

const innerJoin = (collection, separator, rowSeparator) => {
    const result = [];
    const l = collection.length;
    for ( let i = 0; i < l; i++ ){
        if ( !collection[ i ] ){
            continue;
        }
        result.push(collection[ i ].join(separator));
    }
    return result.join(rowSeparator);
};

/**
 * Get a range of values from an collection
 * @param collection
 * @param index1 Start index
 * @param index2 End index (is included in the range)
 * @returns {ArrayBuffer|*|Blob|Array.<T>|string}
 */
const getRange = (collection, index1, index2) => {
    if ( index2 < index1 ){
        [ index1, index2 ] = [ index2, index1 ];
    }
    return collection.slice(index1, index2 + 1);
};

/**
 * High order method that can be used to filter() an array
 * @param property
 */
const filterDuplicates = (...properties) => (item, i, self) => self.find(
    t => properties.every(
        property => t[ property ] == item[ property ])) == item;

const remove = (collection, ...items) => {
    const newCollection = [ ...collection ];
    const l = items.length;
    let item;
    for ( let i = 0; i < l; i++ ){
        item = items[ i ];
        const index = newCollection.indexOf(item);
        if ( index > -1 ){
            newCollection.splice(index, 1);
        }
    }
    return newCollection;
};

const removeFrom = (collection, findCallback) => {
    const index = collection.findIndex(findCallback);
    if ( index < 0 ){
        return;
    }
    collection.splice(index, 1);
};

const addOrRemove = (collection, ...items) => {
    const newCollection = [ ...collection ];
    const l = items.length;
    let item;
    for ( let i = 0; i < l; i++ ){
        item = items[ i ];
        const index = newCollection.indexOf(item);
        if ( index > -1 ){
            newCollection.splice(index, 1);
        }
        else{
            newCollection.push(item);
        }
    }
    return newCollection;
};

const isUnique = (collection, keyValue) => {
    const key = Object.keys(keyValue)[0];
    const occurrences = collection.filter(c => c[key].toLowerCase() === keyValue[key].toLowerCase());
    return occurrences.length === 1;
};

const addUniquesOnly = (collection, ...items) => {
    const uniques = items.filter(item => collection.indexOf(item) == -1);
    return [ ...collection, ...uniques ];
};

const pushIf = (value, condition, collection) => {
    if ( condition ){
        collection.push(value);
    }
};

const addToObjectIf = (source, condition, targetObject) => {
    if ( condition ){
        Object.keys(source).forEach(key => targetObject[ key ] = source[ key ]);
    }
};

const flatten = collection => [].concat(...collection);

/***
 * Get the first key of an object
 * @param target
 * @returns {string}
 */
const getKey = target => Object.keys(target)[0];

/***
 * Get the first value of an object
 * @param target
 * @returns {*}
 */
const getValue = target => target[getKey(target)];

export {
    pushAt,
    innerJoin,
    getRange,
    addOrRemove,
    remove,
    filterDuplicates,
    addUniquesOnly,
    flatten,
    removeFrom,
    pushIf,
    addToObjectIf,
    getKey,
    getValue,
    isUnique
};