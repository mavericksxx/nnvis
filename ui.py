import json
from flask import jsonify
import logging

logger = logging.getLogger(__name__)

class SpectatorMode:
    def __init__(self):
        self.current_generation = 0
        self.top_performers = []
    
    def update_visualization(self, network):
        """Convert network structure to visualization format"""
        neurons = []
        connections = []
        
        # Calculate positions for visualization
        svg_width = 800
        svg_height = 600
        margin = 100
        
        layer_sizes = [len(layer) for layer in network.layers]
        num_layers = len(layer_sizes)
        
        # Calculate spacing
        layer_spacing = (svg_width - 2 * margin) / (num_layers - 1)  # Ensure equal spacing between all layers
        
        # Pre-calculate y-positions for each layer to ensure alignment
        layer_positions = []
        for size in layer_sizes:
            layer_height = svg_height - 2 * margin
            spacing = layer_height / (size + 1)
            positions = [margin + (spacing * (i + 1)) for i in range(size)]
            layer_positions.append(positions)
        
        # Create neurons and connections
        for layer_idx, (layer, y_positions) in enumerate(zip(network.layers, layer_positions)):
            # Calculate x position for this layer
            x = margin + (layer_spacing * layer_idx)
            
            for neuron_idx, (neuron, y) in enumerate(zip(layer, y_positions)):
                neurons.append({
                    'x': x,
                    'y': y,
                    'activation': float(neuron['activation']),
                    'layer_size': len(layer),
                    'layer_index': layer_idx,  # Add layer index for debugging
                    'neuron_index': neuron_idx  # Add neuron index for debugging
                })
                
                # Add connections to next layer
                if layer_idx < len(network.layers) - 1:
                    next_y_positions = layer_positions[layer_idx + 1]
                    next_x = margin + (layer_spacing * (layer_idx + 1))
                    
                    for next_idx, next_y in enumerate(next_y_positions):
                        weight = float(network.weights[layer_idx][neuron_idx][next_idx])
                        connections.append({
                            'source': {'x': x, 'y': y},
                            'target': {'x': next_x, 'y': next_y},
                            'weight': weight,
                            'source_layer': layer_idx,  # Add layer indices for debugging
                            'target_layer': layer_idx + 1
                        })
        
        # Add debug information
        logger.debug(f"Network structure: {layer_sizes}")
        logger.debug(f"Number of neurons per layer: {[len(n) for n in network.layers]}")
        logger.debug(f"Total neurons created: {len(neurons)}")
        logger.debug(f"Total connections created: {len(connections)}")
        
        return {
            'neurons': neurons,
            'connections': connections
        }
    
    def update_leaderboard(self, agents):
        """Update the leaderboard with top performing agents"""
        self.top_performers = sorted(
            agents,
            key=lambda x: x.fitness,
            reverse=True
        )[:10]
        
        return [
            {
                'id': idx,
                'score': float(agent.fitness),  # Convert to float for JSON serialization
                'generation': self.current_generation
            }
            for idx, agent in enumerate(self.top_performers)
        ]

    def get_spectator_data(self):
        """Get current visualization and leaderboard data"""
        try:
            if not self.top_performers:
                logger.debug("No top performers available")
                return jsonify({'error': 'No data available'})
            
            best_network = self.top_performers[0].network
            network_data = self.update_visualization(best_network)
            leaderboard_data = self.update_leaderboard(self.top_performers)
            
            logger.debug(f"Network data: {len(network_data['neurons'])} neurons, "
                        f"{len(network_data['connections'])} connections")
            logger.debug(f"Leaderboard data: {len(leaderboard_data)} entries")
            
            response_data = {
                'network': network_data,
                'leaderboard': leaderboard_data
            }
            
            return jsonify(response_data)
        except Exception as e:
            logger.error(f"Error in get_spectator_data: {str(e)}")
            return jsonify({'error': str(e)}) 