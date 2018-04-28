import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import Input, { InputLabel } from 'material-ui/Input';
import { MenuItem } from 'material-ui/Menu';
import { FormControl, FormHelperText } from 'material-ui/Form';
import Select from 'material-ui/Select';

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
    processor: '',
  };

  handleChange = event => {
    this.setState({ [event.target.name]: event.target.value });
  };

  render() {
    const { classes } = this.props;

    return (
        <FormControl className={styles("").formControl}>
          <InputLabel htmlFor="image-processor">Image Processor</InputLabel>
          <Select
            value={this.state.processor}
            onChange={this.handleChange}
            input={<Input name="age" id="age-helper" />}
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
    );
  }
}

SimpleSelect.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default SimpleSelect;
