//  //********************************** // INTERSECT HEAD // ****************************************//
function intersectHead() {
  
  raycaster.setFromCamera( { x: 0, y: 0 }, camera );
  let intersects = raycaster.intersectObjects( user.children );
  
  if ( intersects.length > 0 ) {
    console.log('head action');
    if ( intersected != intersects[ 0 ].object ) {
      
      if ( intersected ) intersected.material.emissive.setHex( intersected.currentHex );
      
      intersected = intersects[ 0 ].object;
      intersected.currentHex = intersected.material.emissive.getHex();
      intersected.material.emissive.setHex( 0xff0000 );
      // intersected.rotation.y += 0.5;
      // intersected.position.z -= 0.1;
      // let handRay = event.getObjectByName( 'handRay' );
      if (intersected) {
        try {
          sock.send( "sendHaptics" );
        } catch( e ) {
          write( e );
        }
      }
    
    } else {
    
      if ( intersected ) intersected.material.emissive.setHex( intersected.currentHex );

        intersected = undefined;
    
    }
  
  }
}
