import React from 'react';
import { ResponsiveLine } from '@nivo/line'
import {Device_Description} from './device_type.js'

const CustomSymbol = ({ size, color, borderWidth, borderColor }) => (
    <g>
        <circle fill="#fff" r={size / 2} strokeWidth={borderWidth} stroke={borderColor} />
        <circle
            r={size / 5}
            strokeWidth={borderWidth}
            stroke={borderColor}
            fill={color}
            fillOpacity={0.35}
        />
    </g>
)

export class MyGraph extends React.Component {
    render(){
        let ndata = [];
        for (var i=0; i<this.props.data.data.length; i++){
            let idata = this.props.data.data[i];
            let ttime = new Date(idata.time * 1000);
            var stime = ttime.getHours() + ":" + ttime.getMinutes() + ":" + ttime.getSeconds();
            let item ={"x": stime, "y": idata.value};
            ndata.push(item);
        }
        
        return(
            <>
        <ResponsiveLine
            data={[
                {
                    id: 'Data A',
                    data: ndata,
                },
            ]}
            xScale={{
                type: 'time',
                format: '%H:%M:%S',
                useUTC: false,
                min: 'auto',
                max: 'auto',
            }}
            xFormat="time:%H:%M:%S"
                 
            yScale={{ 
                type: 'linear', 
                min: Device_Description[this.props.data.device_type].graph_min,
                max: Device_Description[this.props.data.device_type].graph_max, 
                stacked: false,
                reverse: false 
            }}
            yFormat=" >-.2f"
            curve="monotoneX"
            colors={{ scheme: 'nivo' }}
            axisBottom={{
                format: "%H:%M",
                legend: 'Time',
                legendOffset: 46,
                legendPosition: 'middle'
            }}
            axisLeft={{
                legend: this.props.data.device_type,
                legendPosition: 'middle',
                legendOffset: -40,
            }}
            pointSymbol={CustomSymbol}
            pointSize={10}
            pointBorderWidth={1}
            pointBorderColor={{
                from: 'color',
                modifiers: [['darker', 0.3]],
            }}
            pointLabelYOffset={-12}
            margin={{ top: 50, right: 50, bottom: 50, left: 50 }}
            useMesh={true}
        />
        </>
        );
    }

}