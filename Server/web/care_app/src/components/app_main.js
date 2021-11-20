import React from 'react';
import { Layout, Menu} from 'antd';
import "antd/dist/antd.css";
import {
  SearchOutlined,
  TeamOutlined,
  UserOutlined,
} from '@ant-design/icons';
import UserList from './user_list.js'
import {exceeded_threshold} from './device_type.js'
const { Header, Content, Footer, Sider } = Layout;
var randomColor = require('randomcolor'); // import the script
var https_public_url = "http://127.0.0.1"
var api_base_url = https_public_url + ":8000/";
const wsclient = new WebSocket('ws://127.0.0.1:8000/ws/sensor/RR');

let headers = new Headers();
headers.append('Accept', 'application/json');


const max_array_len = 10;

class MainApp extends React.Component {
  
  constructor(props){
    super(props);
    this.state = {
      collapsed: false,
      flag: false,
      object: ""
    };
    this.OnlineSeniors =  new Map();
    //this.OnlineSeniors.set(temp_user.device_id, temp_user);
  }

  componentDidMount(){

    wsclient.onopen = () => {
      console.log('WebSocket Client Connected');
    };

    wsclient.onclose = (message) => {
      console.log(message);
    };

    wsclient.onerror = (message) => {
      console.log(message);
    };

    wsclient.onmessage = (message) => {
      this.call_back(message);
    };

    fetch(api_base_url + 'get-online-seniors/', {
        method: 'GET',
        headers: headers
    })
    .then((response) => response.json())
    .then((data) => {
      for (var key in data){
        data[key]["watch"] = exceeded_threshold(data[key].data[data[key].data.length - 1].value, data[key].device_type);  // determine whether to add to watch list
        data[key]["color"] = randomColor({luminosity: 'dark',});
        this.OnlineSeniors.set(key, data[key]);
      }
      this.setState({flag: !this.state.flag});  // Triggers a re-rendering
    }).catch(err => {
      console.log(err)
    });

  }

  call_back = e =>  {
    const object = JSON.parse(e.data);
    var jmsg = JSON.parse(object.message);
    if(this.OnlineSeniors.has(jmsg.device_id)) {
      let new_data = {"value": jmsg.value, "time": jmsg.time};
      const time_now = Date.now();
      console.log(jmsg, time_now - jmsg.time);
      this.OnlineSeniors.get(jmsg.device_id).data.push(new_data)
      this.OnlineSeniors.get(jmsg.device_id).watch = exceeded_threshold(
          new_data.value,
          this.OnlineSeniors.get(jmsg.device_id).device_type
      );
      // Maintain array size
      if(this.OnlineSeniors.get(jmsg.device_id).data.length > max_array_len){
        this.OnlineSeniors.get(jmsg.device_id).data.shift();
      }
    }
    this.setState({flag: !this.state.flag});  // Triggers a re-rendering
  };

  onCollapse = collapsed => {
    console.log(collapsed);
    this.setState({ collapsed });
  };

  render() {
    const { collapsed } = this.state;
    return (
      <Layout style={{ minHeight: '100vh' }}>
        <Sider collapsible collapsed={collapsed} onCollapse={this.onCollapse}>
          <div style={{height: 60}}> </div>
          <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline">
            <Menu.Item key="1" icon={<TeamOutlined />}>
              Online Users
            </Menu.Item>
            <Menu.Item key="2" icon={<SearchOutlined />}>
              Search 
            </Menu.Item>
            <Menu.Item key="3" icon={<UserOutlined />}>
              Add New User 
            </Menu.Item>
          </Menu>
        </Sider>
        
        <Layout className="site-layout">
          <Header className="site-layout-background" style={{ padding: 0 }} />
          <Content style={{ margin: '0 16px' }}>
            <div className="site-layout-background" style={{ padding: 24, minHeight: 360 }}>
              <UserList
                online_seniors={Array.from(this.OnlineSeniors.values()).filter(data=>data.watch == false)}
                watch_seniors={Array.from(this.OnlineSeniors.values()).filter(data=>data.watch == true)}
              />
            </div>
          </Content>
          <Footer style={{ textAlign: 'center' }}>NE Lab ©2021 Umass Amherst</Footer>
        </Layout>
      </Layout>
    );
  }
}

export default MainApp;