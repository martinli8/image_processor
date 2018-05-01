import React from 'react';
import { UploadField } from '@navjobs/upload';
import PropTypes from 'prop-types';
import Input, { InputLabel } from 'material-ui/Input';
import { MenuItem } from 'material-ui/Menu';
import { FormControl, FormHelperText } from 'material-ui/Form';
import Select from 'material-ui/Select';
import TextField from 'material-ui/TextField';
import axios from 'axios';
import Button from 'material-ui/Button';
import DownloadLink from "react-download-link";
import Gallery from 'react-photo-gallery';
import Table, { TableBody, TableCell, TableHead, TableRow } from 'material-ui/Table';
import Paper from 'material-ui/Paper';

let id = 0;

const styles = theme => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  formControl: {
    display: 'flex', 
    justifyContent: 'center',
    minWidth: 120,
  },
  selectEmpty: {
    // marginTop: theme.spacing.unit * 2,
  },
  table: {
    minWidth: 700,
  },
});

class SimpleSelect extends React.Component {
  state = {
    currentImageString: '',
    processedImageString: '',
    imagelist: [],
    // currently there is no code to obtain the base64 result of the processed image. This may require some tweaking in the back end, I was thinking about having the post request return it and we can extract it from there (in postData function). Once this is done, set <img src = {this.state.processedImageString}>
    "processor": '',
    "nameTextField": '',
    "message": 'Nothing done yet!',
    "photoset": [],
    "id": 0,
    "Data": []
  };

  createData(user_email, process_req, image_size, process_dur, conv_flag) {
    id += 1;
    return {user_email, process_req, image_size, process_dur, conv_flag};
  }

  assembleData(user_email, process_req, image_size, process_dur, conv_flag)  {
    // console.log('assembleData')
    this.setState({Data: [], id: 0})
    for(var i = 0; i<process_dur.length; i++){
      var arr = this.state.Data
      arr.push(this.createData(user_email, process_req[i], image_size[i], process_dur[i], conv_flag[i]))
    }
    // console.log(arr)
    this.setState({Data: arr})
    console.log(this.state.Data)
  }

  onUpload = (files) => {
    const reader = new FileReader()
    const file = files[0]
    reader.readAsDataURL(file);
    reader.onloadend = () => {
      // console.log(reader.result);
      this.setState({currentImageString: reader.result});
    }
  }

  onNameTextFieldChange = (event) => {
    this.setState({"nameTextField": event.target.value});
  }

  handleChange = event => {
    this.setState({ [event.target.name]: event.target.value });
  };

  onButtonClick = (event) => {
		// console.log(this.state.nameTextField);
    // console.log(this.state.processor);
    // console.log(this.state.currentImageString)
	}

  postData = () => {
    // var db = "http://vcm-3590.vm.duke.edu:5000/api/post_image/"
    var db = "http://127.0.0.1:5000/api/post_image"
    const data = {
      user_email: this.state.nameTextField,
      picture64bit: this.state.currentImageString.split(',')[1],
      process_requested: this.state.processor
    }

    axios.post(db, data).then( (response) => {
        // console.log(response)
        this.setState({"message": response.data});
    }).then(this.getData)
  }

  getData = () => {
    var db = "http://127.0.0.1:5000/api/"+this.state.nameTextField
    const data = {
      user_email: this.state.nameTextField,
      picture64bit: this.state.currentImageString.split(',')[1],
      process_requested: this.state.processor
    }

    axios.get(db).then( (response) => {
        console.log(response)
        this.setState({"imagelist": response.data.processed_image_string});
        this.assembleData(response.data.user_email, response.data.process_requested, response.data.image_size, response.data.process_duration, response.data.conversion_flag)
    }).then(this.updateProcess)
  }

  updateProcess = () => {
    this.setState({"processedImageString": "data:iamge/jpeg;base64,"+this.state.imagelist[this.state.imagelist.length-1]});
    this.setState({photoset: []})
    for(var i = 0; i<this.state.imagelist.length; i++){
      var arr = this.state.photoset
      arr.push({src: "data:iamge/jpeg;base64,"+this.state.imagelist[i], width: 4, height:3})
    }
    console.log(arr)
    this.setState({photoset: arr})
  }


  render() {
    const { classes } = this.props;

    return (
      <div>
				<h2 style={{display: 'flex', justifyContent: 'center'}}>Image Processor</h2>
        <div style={{display: 'flex', justifyContent: 'center'}}>
        <Button>
				<UploadField onFiles={this.onUpload} style={{justifyContent: 'center'}}>
						Upload here
				</UploadField>
        </Button>
        </div>
        <div style={{display: 'flex', justifyContent: 'center'}}>
				<img src={this.state.currentImageString}/>
        <img src={this.state.processedImageString}/>
        </div>
        <div style={{display: 'flex', justifyContent: 'center'}}>
        Please enter your email:
        <TextField
          value={this.state.nameTextField}
          onChange={this.onNameTextFieldChange}/>
        </div>
        <div style={{display: 'flex', justifyContent: 'center'}}>
        <FormControl className={styles("").formControl}>
          <InputLabel htmlFor="image-processor">Image Processor</InputLabel>
          <Select
            value={this.state.processor}
            onChange={this.handleChange}
            input={<Input name="processor" id="image-processor" />}
          >
            <MenuItem value="">
              <em>None</em>
            </MenuItem>
            <MenuItem value={"histogram_eq"}>Histogram Equalization</MenuItem>
            <MenuItem value={"contrast_stretching"}>Contrast Stretching</MenuItem>
            <MenuItem value={"log_compression"}>Log Compression</MenuItem>
            <MenuItem value={"reverse_video"}>Reverse Video</MenuItem>
            <MenuItem value={"edge_detection"}>Edge Detection</MenuItem>
          </Select>
          <FormHelperText>Select a processing method</FormHelperText>
        </FormControl>
        <Button variant="raised" onClick={this.postData} style={{
              backgroundColor: 'grey',
              width:'100px',
              height:'40px',
              textAlign: 'center',
              display: 'flex',
              justifyContent: 'center'}}>
          Upload
        </Button>
        </div>
        <div style={{display: 'flex', justifyContent: 'center'}}>
        {this.state.message}
        </div>
        <div style={{display: 'flex', justifyContent: 'center'}}>
        <Button>
        <a href={this.state.processedImageString} download="filename.jpg" style={{textDecoration: 'none', color: 'black'}}>
            Download Processed Image
        </a>
        </Button>
        </div>
        <div>
        <Gallery photos={this.state.photoset} />
        </div>
        <div>
        <Paper>
          <Table style = {styles.appTable}>
            <TableHead>
              <TableRow>
                <TableCell>User Email</TableCell>
                <TableCell>Process Request</TableCell>
                <TableCell>Image Size</TableCell>
                <TableCell>Process Duration</TableCell>
                <TableCell>Grayscale Conversion</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {this.state.Data.map(n => {
                return (
              <TableRow key={n.id}>
                <TableCell>{n.user_email}</TableCell>
                <TableCell numeric>{n.process_req}</TableCell>
                <TableCell numeric>{n.image_size}</TableCell>
                <TableCell numeric>{n.process_dur}</TableCell>
                <TableCell numeric>{n.conv_flag}</TableCell>
              </TableRow>
                );
                })}
            </TableBody>
          </Table>
          </Paper>
        </div>
        </div>
    );
  }
}

SimpleSelect.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default SimpleSelect;
