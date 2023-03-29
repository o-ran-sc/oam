/*
 * Copyright 2023 highstreet technologies and others
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

const express = require('express');
const router = express.Router();
const fs = require('fs');
const path = require('path');

const directoryPath = 'public/files';
const fileExtensions = ['.sbom.spdx.json', '.vulnerabilities.vex.json'];
const imageList = [];
const severities = [
  { name: 'critical', color: 'red' },
  { name: 'high', color: 'orange' },
  { name: 'medium', color: 'yellow' },
  { name: 'low', color: 'lightblue' },
  { name: 'unknown', color: 'lightgrey' },
  { name: 'none', color: 'lightgrey' }
];
const getScaleFromTotal = (total) => {
  let scale = Math.round(total / 120);
  if (scale < 4) scale = 4;
  if (scale > 10) scale = 10;
  return scale;
}

/* GET home page. */
router.get('/', function (req, res, next) {

  fs.readdir(directoryPath, function (err, files) {
    if (err) {
      console.error('Error reading directory:', err);
      return res.status(500).send('Error reading directory (' + directoryPath + ')');
    }

    const fileList = files.filter(file => file.charAt(0) !== '.').map(file => ({
      name: file,
      type: file.endsWith(fileExtensions[0]) ? 'sbom' : 'vex',
      url: path.join('files', file)
    }));

    const vulnerabilities = (list) => {
      const result = {};
      const data = severities.map((severity, index) => {
        const count = list.filter((vul) => {
          return vul.ratings[0].severity === severity.name;
        }).length
        result[severity.name] = count;
        return { ...severity, count }
      });
      const total = data.reduce((sum, d) => sum + d.count, 0);
      result.scale = getScaleFromTotal(total);

      let angle = 0;
      const slices = data.map((d, i) => {
        const startAngle = i === 0 ? 0 : angle
        angle = startAngle + 2 * Math.PI * (d.count / total)
        const endAngle = angle;
        return { ...d, startAngle, endAngle, arc: endAngle - startAngle > Math.PI ? 1 : 0 }
      });
      result.slices = slices;
      result.count = list.length;
      return result;
    };

    const analyser = (type, file) => {
      const result = {
        url: file
      };
      switch (type) {
        case 'sbom':
          const sbomRawData = fs.readFileSync('./public/' + file);
          const sbom = JSON.parse(sbomRawData);
          result.created = new Date(sbom.creationInfo.created).toISOString().replace('.000Z', 'Z');
          result.packages = sbom.packages.length;
          result.files = sbom.files.length;
          break;
        case 'vex':
          const vexRawData = fs.readFileSync('./public/' + file);
          const vex = JSON.parse(vexRawData);
          result.created = new Date(vex.metadata.timestamp).toISOString().replace('.000Z', 'Z');
          result.components = vex.components.length;
          result.vulnerabilities = vulnerabilities(vex.vulnerabilities);
          break;
        default:
          result.type = type;
      }
      return result;
    };

    fileList.forEach((file) => {
      const imageInfo = file.name.split(':');
      const imageVersion = file.type === 'sbom' ? imageInfo[1].substring(0, imageInfo[1].indexOf(fileExtensions[0])) : imageInfo[1].substring(0, imageInfo[1].indexOf(fileExtensions[1]));
      const exists = imageList.filter((image) => {
        return image.name === imageInfo[0];
      })
      if (exists.length === 0) {
        const imageObj = {
          name: imageInfo[0],
          version: imageVersion
        }
        imageObj[file.type] = analyser(file.type, file.url);
        imageList.push(imageObj);
      } else {
        exists[0][file.type] = analyser(file.type, file.url);
      }
    });

    res.render('index', {
      title: 'Container Analysis',
      date: new Date().toISOString(),
      images: imageList
    });
  });

});
module.exports = router;
