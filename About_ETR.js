import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJs, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend} from 'chart.js';
import data1901 from '../Geo-data/Year-Dataset/data_polygon_1901.json';
import data1902 from '../Geo-data/Year-Dataset/data_polygon_1902.json';
import data1903 from '../Geo-data/Year-Dataset/data_polygon_1903.json';
import data1904 from '../Geo-data/Year-Dataset/data_polygon_1904.json';
import data1905 from '../Geo-data/Year-Dataset/data_polygon_1905.json';
import data1906 from '../Geo-data/Year-Dataset/data_polygon_1906.json';
import data1907 from '../Geo-data/Year-Dataset/data_polygon_1907.json';
import data1908 from '../Geo-data/Year-Dataset/data_polygon_1908.json';
import data1909 from '../Geo-data/Year-Dataset/data_polygon_1909.json';
import data1910 from '../Geo-data/Year-Dataset/data_polygon_1910.json';

import { calculatemean } from '../JS/TimeSeries';
import { type } from '@testing-library/user-event/dist/type';
ChartJs.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);
function About_ETR(){
    var year_select = data1901;
    const [timeSeriesData, setTimeSeriesData] = useState(null);
    const [selectedRegion, setSelectedRegion] = useState('All');
    const [selectedProvince, setSelectedProvince] = useState(''); // จังหวัดที่เลือก
    const [filteredData, setFilteredData] = useState(null); // ข้อมูลที่กรองตามภูมิภาค
    const [provinces, setProvinces] = useState([]); // รายชื่อจังหวัดในภูมิภาค
    const [selectedProvinceData, setSelectedProvinceData] = useState(null);
    const [selectedMonth, setSelectedMonth] = useState(''); // เก็บเดือนที่เลือก
    const [selectedYear, setSelectedYear] = useState('');
    const [selectedData, setSelectedData] = useState(null);
    // const [mean, setmean] = useState(null);
    // const [mmax, setmmax] = useState(null);
    // const [mmin, setmmin] = useState(null);

    const start_year = 1901
    // var result = 0;
    const [dataByYear, setDataByYear] = useState({
        "1901": data1901,
        "1902": data1902,
        "1903": data1903,
        "1904": data1904,
        "1905": data1905,
        "1906": data1906,
        "1907": data1907,
        "1908": data1908,
        "1909": data1909,
        "1910": data1910
    });
    // let month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']; // ป้ายชื่อแกน X (เดือน)
    var m_labels = [];
    var temperature_labels = [];
    const dummyTimeSeriesData = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [
          {
            label: 'Average Temperature (°C)',
            data: [], // เริ่มต้นเป็นอาร์เรย์ว่าง
            borderColor: 'rgba(75,192,192,1)',
            backgroundColor: 'rgba(75,192,192,0.2)',
            fill: true,
            tension: 0.4,
          },
        ],
      };
      const initialData = {
        labels: m_labels,
        datasets: [
            {
              label: 'Average Temperature (°C)', // ชื่อชุดข้อมูล
              data: temperature_labels, // ค่าอุณหภูมิเฉลี่ยแต่ละเดือน
              borderColor: 'rgba(75,192,192,1)', // สีของเส้นกราฟ
              backgroundColor: 'rgba(75,192,192,0.2)', // สีพื้นหลังใต้กราฟ
              fill: true, // เปิดการเติมสีใต้กราฟ
              tension: 0.4, // ความโค้งของเส้นกราฟ
            },
          ],
    }
    const calculatemean = (dataByYear, year) => {
        const geojson = dataByYear[year];
    
        // ตรวจสอบว่า geojson มีโครงสร้างที่ถูกต้อง
        if (!geojson || !geojson.features || !Array.isArray(geojson.features)) {
            console.error(`Invalid GeoJSON data for year ${year}:`, geojson);
            return null;
        }
    
        // สร้างอาร์เรย์เก็บผลรวมและจำนวนข้อมูลของแต่ละเดือน
        const monthlyAverages = Array(12).fill(0);
        const monthlyCounts = Array(12).fill(0);
    
        // วนลูปผ่าน features เพื่อรวบรวมข้อมูล
        geojson.features.forEach((feature) => {
            const { temperature, month } = feature.properties;
    
            // ตรวจสอบว่า month และ temperature มีค่า
            if (month >= 1 && month <= 12 && typeof temperature === 'number') {
            monthlyAverages[month - 1] += temperature;
            monthlyCounts[month - 1] += 1;
            }
        });
    
        // คำนวณค่าเฉลี่ย
        const result = monthlyAverages.map((sum, index) => {
            if (monthlyCounts[index] > 0) {
            return sum / monthlyCounts[index];
            }
            return null; // ไม่มีข้อมูลในเดือนนี้
        });
    
        console.log(`Monthly Average Temperatures for the Year ${year}:`, result);
    
        // อัปเดตค่าใน dummyTimeSeriesData
        dummyTimeSeriesData.datasets[0].data = result;
    
        console.log('Updated dummyTimeSeriesData:', dummyTimeSeriesData);
    
        return result;
    };
    const [chartData, setChartData] = useState(initialData);
    useEffect(() => {
        // ถ้ามีการเลือกปีแล้ว อัปเดตกราฟ
        if (selectedYear) {
          const result = calculatemean(dataByYear, selectedYear);
        //   setmean(result);
        //   console.log('loop'+result)
          if (result) {
            setChartData({ ...dummyTimeSeriesData, datasets: [{ ...dummyTimeSeriesData.datasets[0], data: result }] });
          }
        }
      }, [selectedYear]);
    var arr = calculatemean(dataByYear, selectedYear)
    let mean = [];
    for (let key in arr){
        mean.push(arr[key]);
    }
    // console.log(typeof(mean))
    // let arr = Object.keys(mean).map(key => mean[key])
    // let arr = [...Object.values(mean)];
    // console.log(mean[0])
    // for (let i = 0; i < mean.length;i+=1){
    //     console.log(mean[i])
    // }
    // let arr = Object.values(mean)
    // console.log(arr)
    // let mmax = Math.max(arr)
    // console.log(mmax)
    // setmmin(mean[0])
    // setmmax(mean[0])
    var mmax = mean[0];
    var mmin = mean[0];
    for (let i = 0; i < mean.length;i+=1){
        // console.log(mean[i])
        if(mmin > mean[i]){
            mmin = mean[i];
            // console.log(mmin)
            // console.log(mean[i])
            // setmmin(mean[i]);
        }else if(mmin < mean[i]){
            mmin = mmin;
            // setmmin(mmin);
        }
    }
    for (let i = 0; i < mean.length;i+=1){
        if(mmax < mean[i]){
            mmax = mean[i];
        }else if(mmax > mean[i]){
            mmax = mmax;
        }
    }
    console.log(mmax)
    console.log(mmin)
    // console.log(mmax-mmin)
    // console.log(selectedYear);
    // for(let i = 1; i < 13;i+=1){ 
    //     for(let j = 0; j <= year_select.features.length - 1;j+=1){
    //         if (year_select.features[j].properties['region'] == 'North_region'){
    //             // console.log(j, month_labels[year_select.features[j].properties['month']-1], year_select.features[i].properties['name']);
    //             if(year_select.features[j].properties['month'] == i){
    //                 console.log(i, year_select.features[j].properties['name']);
    //             }
    //         }
    //     }
    // }

    // for(let j = 0; j <= year_select.features.length - 1;j+=1){
    //     year_select.features[i].properties['temperature']
    //     if (data1901.features[i].properties['name'] == 'Chiang Rai'){
    //     if (data1901.features[i].properties['name'] == 'Chiang Mai'){
    //         m_labels.push(month_labels[data1901.features[i].properties['month']-1])
    //         temperature_labels.push(data1901.features[i].properties['temperature'])
    //         console.log(month_labels[data1901.features[i].properties['month']-1], data1901.features[i].properties['temperature'])
    //         console.log(data1901.features[i].properties['region'])
    //     }
    // }
    
    

    // const filterByRegion = (data, region) =>{
    //     return data.features;
    // }
    
    return(
        <div className="main-container">
            Extreme temperature range<br/>
            Let TXx be the daily maximum temperature in month k and TNn the daily minimum temperature in month k. The extreme temperature range each month is then:
            
            <div className="month-selector">
                <label>Select Month</label>
                <select onChange={(e) => {
                    const selectedMonth = parseInt(e.target.value, 10);
                    setSelectedMonth(selectedMonth);  // กำหนดเดือนที่เลือก
                }}
                value={selectedMonth}
                style={{width:'200px', padding: '10px', fontSize:'16px'}}>
                    <option value='1'>January</option>
                    <option value='2'>February</option>
                    <option value='3'>March</option>
                    <option value='4'>April</option>
                    <option value='5'>May</option>
                    <option value='6'>June</option>
                    <option value='7'>July</option>
                    <option value='8'>August</option>
                    <option value='9'>September</option>
                    <option value='10'>October</option>
                    <option value='11'>November</option>
                    <option value='12'>December</option>

                </select>
            </div>
            <div className="year-selector">
            <label>Selected Year</label>
            <select
                onChange={(e) => {
                    const selectedYear = parseInt(e.target.value, 10);
                    setSelectedYear(selectedYear)
                }}
                // onChange={handleYearChange}
                style={{width:'200px', padding: '10px', fontSize:'16px'}}>
                    <option value=''>All Year</option>
                    {[...Array(123).keys()].map((year) => (
                    <option key={year} value={start_year+year}>
                        {`${start_year+year}`}
                    </option>
                    ))}

                </select>
                {/* {typeof(String(selectedYear))} */}
                {/* <select
                    // onChange={handleYearChange}
                    value={selectedYear}
                    style={{ width: '200px', padding: '10px', fontSize: '16px' }}
                >
                    <option value="">-- Selected Year --</option>
                    {Object.keys(dataByYear).map((year) => (
                    <option key={year} value={year}>
                        {year}
                    </option>
                    ))}
                </select> */}
            </div>
            <div className="region-selector">
            <label>Select Region:</label>
            <select 
                onChange={(e) => setSelectedRegion(e.target.value)} 
                value={selectedRegion} 
                style={{ width: '200px', padding: '10px', fontSize: '16px' }}
            >
                <option value="All">All Regions</option>
                <option value="North_East_region">North East</option>
                <option value="North_region">North</option>
                <option value="South_region">South</option>
                <option value="Middle_region">Middle</option>
                <option value="East_region">East</option>
                <option value="West_region">West</option>
            </select>
            </div>
            <div>
                <p>
                    highest temperature : {mmax}<br/>
                    lowest temperature : {mmin}<br/>
                    ETR range : {mmax-mmin}
                </p>                
            </div>
            <div style={{width:'80%', height:'400px',margin:'0 auto'}}>
                <Line data={chartData}
                options={{
                    responsive: true, // ให้กราฟปรับขนาดตามหน้าจอ
                    plugins: {
                      legend: {
                        display: true, // แสดงคำอธิบายชุดข้อมูล
                        position: 'top', // ตำแหน่งคำอธิบายอยู่ด้านบน
                      },
                    },
                    scales: {
                      x: {
                        beginAtZero: true, // แกน X เริ่มต้นที่ 0
                      },
                      y: {
                        beginAtZero: true, // แกน Y เริ่มต้นที่ 0
                      },
                    },
                  }}
                />
            </div>
            
        </div>
        
    );
}
export default About_ETR;