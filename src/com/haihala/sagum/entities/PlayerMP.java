package com.haihala.sagum.entities;

import java.net.InetAddress;

import com.haihala.sagum.InputHandler;
import com.haihala.sagum.level.Level;

public class PlayerMP extends Player {

    public InetAddress ipAddress;
    public int port;

    public PlayerMP(Level level, int x, int y, InputHandler input, String username, InetAddress ipAddress, int port) {
        super(level, x, y, input, username);
        this.ipAddress = ipAddress;
        this.port = port;
    }

    public PlayerMP(Level level, int x, int y, String username, InetAddress ipAddress, int port) {
        super(level, x, y, null, username);
        this.ipAddress = ipAddress;
        this.port = port;
    }

    @Override
    public void tick() {
        super.tick();
    }


    public String printString(){
        return super.printString() + " ip:"+this.ipAddress + " port"+this.port;
    }
}
