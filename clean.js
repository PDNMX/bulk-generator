const fs = require('fs');

const clean = () => {
  const dir = `${__dirname}/data`;
  if (fs.existsSync(dir)) fs.rmSync(dir, { recursive: true });
};

clean();
