const db = require('../persistence');

module.exports = async (req, res) => {
    const updatedFields = {
        name: req.body.name,
        completed: req.body.completed,
        favorite: req.body.favorite, // Add support for 'favorite'
    };

    await db.updateItem(req.params.id, updatedFields);
    const item = await db.getItem(req.params.id);
    res.send(item);
};

// const db = require('../persistence');

// module.exports = async (req, res) => {
//     await db.updateItem(req.params.id, {
//         name: req.body.name,
//         completed: req.body.completed,
//     });
//     const item = await db.getItem(req.params.id);
//     res.send(item);
// };
