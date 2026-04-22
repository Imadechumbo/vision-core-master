const express = require('express');
const router = express.Router();

router.post('/api/v1/chat/vision', async (req, res) => {
  const mime = req.file.mimetype;
  return res.json({ ok: true, mime });
});

module.exports = router;