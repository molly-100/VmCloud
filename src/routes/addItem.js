const db = require('../persistence');
const {v4 : uuid} = require('uuid');

module.exports = async (req, res) => {
    const item = {
        id: uuid(),
        name: req.body.name,
        dateTime: req.body.dateTime,
        completed: false,
    };

    await db.storeItem(item);
    res.send(item);
};
