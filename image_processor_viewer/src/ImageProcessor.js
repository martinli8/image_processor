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

const styles = theme => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  formControl: {
    // margin: theme.spacing.unit,
    minWidth: 120,
  },
  selectEmpty: {
    // marginTop: theme.spacing.unit * 2,
  },
});

class SimpleSelect extends React.Component {
  state = {
    currentImageString: '',
    processedImageString: '',
    // currently there is no code to obtain the base64 result of the processed image. This may require some tweaking in the back end, I was thinking about having the post request return it and we can extract it from there (in postData function). Once this is done, set <img src = {this.state.processedImageString}>
    "processor": '',
    "nameTextField": '',
    "message": 'Nothing done yet!',
  };

  onUpload = (files) => {
    const reader = new FileReader()
    const file = files[0]
    reader.readAsDataURL(file);
    reader.onloadend = () => {
      console.log(reader.result);
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
		console.log(this.state.nameTextField);
    console.log(this.state.processor);
    console.log(this.state.currentImageString)
	}

  postData = () => {
    var db = "http://vcm-3590.vm.duke.edu:5000/api/post_image/"

    const data = {
      user_email: this.state.nameTextField,
      picture64bit: this.state.currentImageString.split(',')[1],
      process_requested: this.state.processor
    }

    axios.post(db, data).then( (response) => {
        console.log(response)
        this.setState({"message": data});
    })
  }

  render() {
    const { classes } = this.props;

    return (
      <div>
				<h2>Upload your image</h2>
				<UploadField onFiles={this.onUpload}>
					<div style={{
							backgroundColor: 'gray',
							width:'200px',
							height:'200px',
							textAlign: 'center'}}>
						Upload here
					</div>
				</UploadField>
				<img src={this.state.currentImageString} alt = "Pre-processed image" />

        <TextField
          value={this.state.nameTextField}
          onChange={this.onNameTextFieldChange}/>

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

        <Button variant="raised" onClick={this.postData}>
					Upload
				</Button>
        {this.state.message}
        </div>


    );
  }
}

SimpleSelect.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default SimpleSelect;
