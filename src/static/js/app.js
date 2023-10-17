function App() {
    const { Container, Row, Col } = ReactBootstrap;
    return (
        <Container>
            <Row>
                <Col md={{ offset: 3, span: 6 }}>
                    <TodoListCard />
                </Col>
            </Row>
        </Container>
    );
}

function TodoListCard() {
    const [items, setItems] = React.useState(null);

    React.useEffect(() => {
        fetch('/items')
            .then(r => r.json())
            .then(setItems);
    }, []);

    const onNewItem = React.useCallback(
        newItem => {
            setItems([...items, newItem]);
        },
        [items],
    );

    const onItemUpdate = React.useCallback(
        item => {
            const index = items.findIndex(i => i.id === item.id);
            setItems([
                ...items.slice(0, index),
                item,
                ...items.slice(index + 1),
            ]);
        },
        [items],
    );

    const onItemRemoval = React.useCallback(
        item => {
            const index = items.findIndex(i => i.id === item.id);
            setItems([...items.slice(0, index), ...items.slice(index + 1)]);
        },
        [items],
    );

    if (items === null) return 'Loading...';

    //TEST CODE
    const toggleFavourite = (item) => {
        fetch(`/items/${item.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                name: item.name,
                completed: item.completed,
                favourite: !item.favourite, // Toggle the favourite status
            }),
            headers: { 'Content-Type': 'application/json' },
        })
            .then((response) => response.json())
            .then((updatedItem) => {
                const updatedItems = items.map((i) =>
                    i.id === updatedItem.id ? updatedItem : i
                );
                setItems(updatedItems);
            });
    };

    return (
        <React.Fragment>
            <AddItemForm onNewItem={onNewItem} />
            {items.length === 0 && (
                // <p className="text-center">No items yet! Add one above!</p>
                <p className="text-center">You have no todo items yet! Add one above!</p>
            )}
            {items.map(item => (
                <ItemDisplay
                    item={item}
                    key={item.id}
                    onItemUpdate={onItemUpdate}
                    onItemRemoval={onItemRemoval}
                    toggleFavourite={toggleFavourite} // Pass the toggleFavorite function
                />
            ))}
        </React.Fragment>
    );
}

function AddItemForm({ onNewItem }) {
    const { Form, InputGroup, Button } = ReactBootstrap;

    const [newItem, setNewItem] = React.useState('');
    const [submitting, setSubmitting] = React.useState(false);

    const submitNewItem = e => {
        e.preventDefault();
        setSubmitting(true);
        fetch('/items', {
            method: 'POST',
            body: JSON.stringify({ name: newItem }),
            headers: { 'Content-Type': 'application/json' },
        })
            .then(r => r.json())
            .then(item => {
                onNewItem(item);
                setSubmitting(false);
                setNewItem('');
            });
    };

    return (
        <Form onSubmit={submitNewItem}>
            <InputGroup className="mb-3">
                <Form.Control
                    value={newItem}
                    onChange={e => setNewItem(e.target.value)}
                    type="text"
                    placeholder="New Item"
                    aria-describedby="basic-addon1"
                />
                <InputGroup.Append>
                    <Button
                        type="submit"
                        variant="success"
                        disabled={!newItem.length}
                        className={submitting ? 'disabled' : ''}
                    >
                        {submitting ? 'Adding...' : 'Add Item'}
                    </Button>
                </InputGroup.Append>
            </InputGroup>
        </Form>
    );
}

function ItemDisplay({ item, onItemUpdate, onItemRemoval, toggleFavourite }) {
    const { Container, Row, Col, Button } = ReactBootstrap;

    const toggleCompletion = () => {
        fetch(`/items/${item.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                name: item.name,
                completed: !item.completed,
            }),
            headers: { 'Content-Type': 'application/json' },
        })
            .then(r => r.json())
            .then(onItemUpdate);
    };

    const removeItem = () => {
        fetch(`/items/${item.id}`, { method: 'DELETE' }).then(() =>
            onItemRemoval(item),
        );
    };

    return (
        <Container fluid className={`item ${item.completed && 'completed'}`}>
            <Row>
                <Col xs={1} className="text-center">
                    <Button
                        //className="toggles"
                        className={`toggles ${item.favourite ? 'favourite' : ''}`}
                        size="sm"
                        variant="link"
                        //onClick={toggleCompletion}
                        onClick={toggleFavourite} // Use the toggleFavourite function
                        aria-label={
                            //item.completed
                            item.favourite
                                ? 'Remove from favourites'
                                : 'Add to favourites'
                                // ? 'Mark item as incomplete'
                                // : 'Mark item as complete'
                        }
                    >
                        <i
                            className={`far ${item.favorite ? 'fa-star' : 'fa-star-o'}`}
                            // className={`far ${
                            //     item.completed ? 'fa-check-square' : 'fa-square'
                            // }`}
                        />
                    </Button>
                </Col>

                //     ADDED CODE
                <Col xs={10} className="name">
                    <span
                        style={{
                            color: item.favorite ? 'darkblue' : 'black',
                            paddingRight: '10px',
                        }}
                    >
                        {item.name}
                    </span>
                    {item.favorite && (
                        <i
                            className="fa fa-star"
                            style={{ color: 'gold' }} // Adjust the star color
                        />
                    )}
                </Col>

                        
                <Col xs={10} className="name">
                    {item.name}
                </Col>
                <Col xs={1} className="text-center remove">
                    <Button
                        size="sm"
                        variant="link"
                        onClick={removeItem}
                        aria-label="Remove Item"
                    >
                        <i className="fa fa-trash text-danger" />
                    </Button>
                </Col>
            </Row>
        </Container>
    );
}

ReactDOM.render(<App />, document.getElementById('root'));
