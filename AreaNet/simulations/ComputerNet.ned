//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 

package areanet.simulations;
import areanet.Computer;
import areanet.Multiplexer;
import areanet.BandwidthProvider;
import areanet.Service;

network ComputerNet
{
    @display("bgb=585.344,533.696");
    submodules:
        bwprovider: BandwidthProvider {
            @display("i=device/antennatower_vl;p=269,87");
        }
        multiplexer: Multiplexer {
            @display("i=device/device_l;p=269,223");
        }
        App_UserA: Computer {
            @display("i=device/pc;p=128,319");
        }
        App_UserB: Computer {
            @display("i=device/pc;p=219,332");
        }
        App_UserC: Computer {
            @display("i=device/pc;p=411,311");
        }
        App_UserD: Computer {
            @display("i=device/pc;p=319,332");
        }
        consumerService1: Service {
            @display("i=device/server,p,194,455;p=179,455");
        }
        consumerService2: Service {
            @display("i=device/server2,p,395,455;p=380,455");
        }
    connections:
        bwprovider.out --> multiplexer.in;
        multiplexer.out[0] --> App_UserA.in;
        multiplexer.out[1] --> App_UserB.in;
        multiplexer.out[2] --> App_UserC.in;
        multiplexer.out[3] --> App_UserD.in;
        App_UserA.out --> consumerService1.in[0];
        App_UserB.out --> consumerService1.in[1];
        App_UserC.out --> consumerService2.in[0];
        App_UserD.out --> consumerService2.in[1];

}
