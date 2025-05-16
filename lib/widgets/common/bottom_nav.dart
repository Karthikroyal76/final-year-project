import 'package:flutter/material.dart';

class BottomNavItem {
  final IconData icon;
  final String label;

  BottomNavItem({required this.icon, required this.label});
}

class CustomBottomNav extends StatelessWidget {
  final int currentIndex;
  final Function(int) onTap;
  final List<BottomNavItem> items;
  final Color? backgroundColor;
  final Color? selectedItemColor;
  final Color? unselectedItemColor;

  const CustomBottomNav({
    super.key,
    required this.currentIndex,
    required this.onTap,
    required this.items,
    this.backgroundColor,
    this.selectedItemColor,
    this.unselectedItemColor,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: backgroundColor ?? Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.2),
            spreadRadius: 1,
            blurRadius: 4,
            offset: Offset(0, -1),
          ),
        ],
      ),
      child: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 8.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: items.asMap().entries.map((entry) {
              final index = entry.key;
              final item = entry.value;
              final isSelected = index == currentIndex;
              
              return InkWell(
                onTap: () => onTap(index),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      item.icon,
                      color: isSelected 
                          ? selectedItemColor ?? Theme.of(context).primaryColor
                          : unselectedItemColor ?? Colors.grey,
                    ),
                    const SizedBox(height: 4.0),
                    Text(
                      item.label,
                      style: TextStyle(
                        fontSize: 12.0,
                        color: isSelected 
                            ? selectedItemColor ?? Theme.of(context).primaryColor
                            : unselectedItemColor ?? Colors.grey,
                        fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                      ),
                    ),
                  ],
                ),
              );
            }).toList(),
          ),
        ),
      ),
    );
  }
}