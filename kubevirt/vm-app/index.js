const express = require('express');
const mongoose = require('mongoose');
const app = express();


const dbURI = 'mongodb://vm-app-svc:27017/example';

app.use(express.json());
app.get('/', (req, res) => {
  return res.send('Hello World!');
});

app.post('/', async (req, res) => {
  return res.send(await Person.create(req.body));
});
app.get('/all', async (req, res) => {
  try {
    return res.send(await Person.find());

  } catch (e) {
    console.log(e.message);
  }
});

app.get('/:id', async (req, res) => {
  return res.send(await Person.findById(req.params.id));
});

const schema = new mongoose.Schema({
  name: String,
  age: Number,
  address: String,
});
const Person = mongoose.model('Person', schema);

app.listen(3000, async () => {
  console.log('Example app listening on port 3000!');
  try {
    mongoose.set("strictQuery", false);
    console.log("Connecting to db: " + dbURI);
    await mongoose.connect(dbURI);
    console.log("Connected to DB");
  } catch (e) {
      console.error("Failed to connect to DB");
      process.exit(1);
  }

});

