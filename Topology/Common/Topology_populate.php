<?php

function _topology_exist_object_this_instance($nodeId) {
	global $context;
	
	foreach($context['Nodes'] as $key => $value) {
		if($value["object_id"] == $nodeId) {
			return $key;
		}
	}
	return -1;
}

function createTopology($nodeId, $name, $device_nature, $subtype, $image) {
	global $context;
	
	$place = _topology_exist_object_this_instance($nodeId);

	logTofile("*** createTopology 1  nodeId $nodeId,  name $name place: $place");

	if ($place == -1) {
		$context['Nodes'][] = array(
			"primary_key" => $nodeId,
			"device_nature" => $device_nature,
			"name" => $name,
			"object_id" => $nodeId,
			"x" => "",
			"y" => "",
			"description" => "",
			"subtype" => $subtype,
			"image" => $image,
			"color" => "#acd7e5",
			"hidden" => "false",
			"cluster_id" => ""
		);

		$place = _topology_exist_object_this_instance($nodeId);
	} else {
		unset($context['Nodes'][$place]["link"]);
		$context['Nodes'][$place]["name"] = $name;
		$context['Nodes'][$place]["image"] = $image;
	}
	logTofile("*** createTopology  2 nodeId $nodeId,  name $name place: $place");

	$context['Nodes_MAJ'][] = array(
			"object_id" => $nodeId,
			"primary_key" => $nodeId
	);
	logTofile("*** createTopology 3 nodeId: ".$nodeId. " name " .$name." subtype ". $subtype." place ". $place."\n");
	logTofile(debug_dump($context, "*** createTopology context \n"));

	return $place;
}

function createTopologyNetwork($nodeId, $name, $subtype, $image) {
	global $context;

	$place = _topology_exist_object_this_instance($nodeId);
	if ($place == -1) {
		$context['Nodes'][] = array(
			"primary_key" => $nodeId,
			"name" => $name,
			"object_id" => $nodeId,
			"x" => "",
			"y" => "",
			"description" => "",
			"subtype" => $subtype,
			"image" => $image,
			"color" => "#acd7e5",
			"hidden" => "false",
			"cluster_id" => ""
		);

		$place = _topology_exist_object_this_instance($nodeId);
	} else {
		unset($context['Nodes'][$place]["link"]);
		$context['Nodes'][$place]["name"] = $name;
		$context['Nodes'][$place]["image"] = $image;
	}

	$context['Nodes_MAJ'][] = array(
			"object_id" => $nodeId,
			"primary_key" => $nodeId
	);
	logTofile("***  createTopologyNetwork nodeId: ".$nodeId. " name " .$name." subtype ". $subtype." place ". $place."\n");
	//logTofile(debug_dump($context, "*** createTopologyNetwork context ***"));

	return $place;
}


?>