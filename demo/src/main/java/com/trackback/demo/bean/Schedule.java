package com.trackback.demo.bean;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import java.sql.Timestamp;

@Entity
public class Schedule {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Integer id;
    private float longitude;
    private float latitude;
    private Timestamp time;
    private Integer conditions;
    private Integer remain;
    private Integer driverid;

    public Schedule(){}

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

    public void setConditions(Integer conditions){
        this.conditions = conditions;
    }

    public Integer getConditions(){
        return conditions;
    }

    public void setRemain(Integer remain){
        this.remain = remain;
    }

    public Integer getRemain(){
        return remain;
    }

    public void setDriverid(Integer driverid){
        this.driverid = driverid;
    }

    public Integer getDriverid(){
        return driverid;
    }
}
