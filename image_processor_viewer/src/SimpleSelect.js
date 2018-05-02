import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import Input, { InputLabel } from 'material-ui/Input';
import { MenuItem } from 'material-ui/Menu';
import { FormControl, FormHelperText } from 'material-ui/Form';
import Select from 'material-ui/Select';
import TextField from 'material-ui/TextField';

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
    "processor": '',
    "nameTextField": '',
  };

  onNameTextFieldChange = (event) => {
    this.setState({"nameTextField": event.target.value});
  }

  handleChange = event => {
    this.setState({ [event.target.name]: event.target.value });
  };

  render() {
    const { classes } = this.props;

    return (
      <div>
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
        </div>
    );
  }
}

SimpleSelect.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default SimpleSelect;
