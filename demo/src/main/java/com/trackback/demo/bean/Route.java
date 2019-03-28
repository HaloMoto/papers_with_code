package com.trackback.demo.bean;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import java.sql.Timestamp;

@Entity
public class Route {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Integer id;
    private float longitude;
    private float latitude;
    private Timestamp time;
    private Integer driverid;

    public Route(){}

    public void setId(Integer id){
        this.id = id;
    }

    public Integer getId(){
        return id;
    }

    public void setLongitude(float longitude){
        this.longitude = longitude;
    }

    public float getLongitude(){
        return longitude;
    }

    public void setLatitude(float latitude){
        this.latitude = latitude;
    }

    public float getLatitude(){
        return latitude;
    }

    public void setTime(Timestamp time){
        this.time = time;
    }

    public Timestamp getTime(){
        return time;
    }

    public void setDriverid(Integer driverid){
        this.driverid = driverid;
    }

    public Integer getDriverid(){
        return driverid;
    }
}
