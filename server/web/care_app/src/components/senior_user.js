import React from 'react';
import { Avatar,  Typography, Row, Col, Divider, Modal} from 'antd';
import "antd/dist/antd.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMars, faVenus,} from '@fortawesome/free-solid-svg-icons'
import {Device_Tile, Device_Modal} from './device_type.js'

const { Text } = Typography;
var randomColor = require('randomcolor'); // import the script

class SeniorUser extends React.Component {
  
  constructor(props){
    super(props);
    this.state = {
      collapsed: false,
      isModalVisible: false,
    };  
  }

  componentDidMount(){ }

  senior_object = () => {

    const bulk_watch_style = {fontSize: 14, fontWeight: "bold", color: this.props.textVisible ? '#ff0800' : '#dcdcdc', padding: 2, borderRadius: 4,};
    const bulk_normal_style = {fontSize: 14, padding: 2}; 

    return (  
      <>{ 
      this.props.element_size === 1 ?

        <Row>  {/***  Normal Mode ****/}
          {/* Avatar */}
          <Col flex={1}> 
            <Avatar size={24} style={{ marginRight:5, backgroundColor: this.props.data.color}}  >{this.props.data.name[0]}</Avatar>           
          </Col>

          {/* Name and Device ID*/}
          <Col flex={5}>  
            <Row> <Text strong style={{fontSize: 13}}> {this.props.data.name.substr(0, 16)} </Text> </Row>
            <Row justify='space-around'> 
              <Col flex={1}>
                <Text code >
                    {this.props.data.gender === 'male' ?
                        <FontAwesomeIcon icon={faMars} size="1x"/> :
                        <FontAwesomeIcon icon={faVenus} size="1x"/>
                    }
                </Text>
              </Col >
              <Col flex={5}>
                <Text disabled style={{fontSize: 10, textAlign: 'center'}}> {'@'+this.props.data.device_id} </Text> 
              </Col>
            </Row>
          </Col>

          {/* Device Data */}
          <Col flex={3}>
            <Row justify='space-around'>
              <Col  >
                <Row justify='space-around'>
                  <Text code style={{textAlign: 'center'}}> 
                    {this.props.data.battery + '%' + '🔋'}  
                  </Text>
                </Row>
              </Col>
              <Col >
                  <Divider type="vertical" style={{ margin: 0, height: '100%'}}/>
              </Col>
              <Col > 
                <Device_Tile 
                  device_type={this.props.data.device_type} 
                  current_data={this.props.data.data[ this.props.data.data.length - 1].value}
                  size={this.props.element_size}
                  watch={this.props.data.watch}
                  textVisible={this.props.textVisible}
                />
              </Col>
            </Row>
          </Col>
        </Row>      

      : 
        <Row justify='space-around'>  {/***  Bulk Mode ****/}
          {/* Avatar */}
          <Col> 
            <Avatar size={16} style={{ marginRight:0, backgroundColor: this.props.data.color}}  >{this.props.data.name[0]}</Avatar>           
          </Col>
          
          <Col> 
            <Text style={{fontSize: 10, textAlign: 'center'}}> 
              {this.props.data.device_type}: 
            </Text> 
            <Text code style={this.props.data.watch ? bulk_watch_style : bulk_normal_style}>
              {this.props.data.data[ this.props.data.data.length - 1].value}
            </Text> 
          </Col>
        </Row>
    }</>
    ) 
  }

  MouseOver = (event) =>{
    event.currentTarget.style.boxShadow = "1px 1px 1px 0px " + this.props.data.color;
  }

  MouseOut = (event) =>{
    event.currentTarget.style.boxShadow = "2px 2px 2px 2px #dcdcdc";
  }

  ModelClose = () =>{
    this.setState({isModalVisible: false});
  }

  ModelOpen = () =>{
    this.setState({isModalVisible: true});
  }

  render() {
    return (

      <>
      <div 
        style = { this.props.element_size === 1 ? styles.card_div : styles.card_div_small} 
        flex ='auto'
        onClick = {this.ModelOpen} 
        onMouseOver={this.MouseOver} onMouseOut={this.MouseOut}
      >
        {this.senior_object()}
      </div>
        
      <Modal
          visible={this.state.isModalVisible} 
          onOk={this.ModelClose} 
          onCancel={this.ModelClose} 
          width={'60%'}
          title="More ..."
        >
          <Device_Modal {...this.props}/>
      </Modal>

      </>
    );
  }
}

export default SeniorUser;


const styles = {
  card_div:{
    borderRadius: 10, 
    margin: 5,
    padding: 10,
    backgroundColor: 'white',
    boxShadow: "2px 2px 2px 2px #dcdcdc",
    cursor: "pointer",
    
  },
  card_div_small:{
    borderRadius: 5, 
    margin: 2,
    padding: 3,
    backgroundColor: 'white',
    boxShadow: "2px 2px 2px 2px #dcdcdc",
    cursor: "pointer",
  },
  batteryIcon:{
     marginLeft: 8,
  }
}

