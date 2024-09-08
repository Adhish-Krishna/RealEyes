import express from 'express';
import multer from 'multer';
import path from 'path';
import bodyParser from 'body-parser';
import fs from 'fs';
import axios from 'axios';
import { dirname } from 'path';
import { fileURLToPath } from 'url';
import FormData from 'form-data';

const app = express();
const port = 3000;
const __dirname = dirname(fileURLToPath(import.meta.url));
app.use(express.static("public"));
app.use(bodyParser.urlencoded({extended:true}));

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        cb(null, uniqueSuffix + path.extname(file.originalname));
    }
});

const upload = multer({ storage: storage });

const uploadDir = './uploads';
if (!fs.existsSync(uploadDir)){
    fs.mkdirSync(uploadDir);
}

app.get("/",(req,res)=>{
  res.render("index.ejs");
})

app.get("/text" , (req,res)=>{
    res.render("text.ejs");
})

app.get("/audio",(req,res)=>{
    res.render("audio.ejs");
})

app.get("/visualmedia",(req,res)=>{
    res.render("image.ejs");
})

app.post("/text", upload.none(), async (req, res) => {
    const { text } = req.body;
    try {
        let response = await axios.post(" http://127.0.0.1:8000/classify", {
            text: text
        });
        let confidence = response.data.confidence;
        confidence = parseInt(parseFloat(confidence * 100));
        response.data.confidence = confidence;
        res.send(response.data);
    } catch (error) {
        res.send(error);
    }
});

app.post('/detect', upload.single('file'), async (req, res) => {
    let filePath;
  if (!req.file) {
      return res.status(400).send('No file uploaded.');
  }
  try {
      filePath = path.join(__dirname, 'uploads', req.file.filename);
      const formData = new FormData();
      formData.append('file', fs.createReadStream(filePath));
      let apiUrl;
      if (req.file.mimetype.startsWith('image/')) {
          apiUrl = 'http://127.0.0.1:5000/predict';
      } else if (req.file.mimetype.startsWith('video/')) {
          apiUrl = 'http://127.0.0.1:5000/predict/video';
      } else {
          return res.status(400).send('Unsupported file type.');
      }
      const response = await axios.post(apiUrl, formData, {
          headers: {
              ...formData.getHeaders()
          }
      });
      if (req.file.mimetype.startsWith('video/')) {
          const consolidatedResponse = {
              predictions: response.data.map(pred => ({
                  prediction: pred.prediction,
                  probability: pred.probability
              }))
          };
          console.log(consolidatedResponse);

          res.send(consolidatedResponse);
      } else {
          res.send(response.data);
      }
  } catch (error) {
      console.error('Error forwarding file:', error.message);
      res.status(500).send('Error forwarding file to the detection API.');
  }finally {
    fs.unlink(filePath, (err) => {
        if (err) {
            console.error('Error deleting file:', err.message);
        } else {
            console.log('File deleted successfully.');
        }
    });
}
});

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
